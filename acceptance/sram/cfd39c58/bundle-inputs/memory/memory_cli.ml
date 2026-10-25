open! Core
open Hardcaml_asic

let usage =
  "Usage: memory_cli (check|emit) --selection (flops|exact)\n\
   \       emit also requires --source-root ROOT --output-dir NEW_OR_EMPTY_DIR\n"
;;

let () =
  let bad () = Out_channel.output_string stderr usage; Stdlib.exit 2 in
  let args = Array.to_list (Sys.get_argv ()) |> List.tl_exn in
  match args with
  | [ "--help" ] -> Out_channel.output_string stdout usage
  | command :: rest when List.mem [ "check"; "emit" ] command ~equal:String.equal ->
    let rec parse acc = function
      | [] -> acc
      | key :: value :: rest
        when List.mem [ "--selection"; "--source-root"; "--output-dir" ] key ~equal:String.equal
             && not (List.Assoc.mem acc key ~equal:String.equal) ->
        parse ((key, value) :: acc) rest
      | _ -> bad ()
    in
    let options = parse [] rest in
    let get key = List.Assoc.find options key ~equal:String.equal in
    let requirement =
      match get "--selection" with
      | Some "flops" -> Resource_policy.Requirement.Flops
      | Some "exact" -> Exact
      | _ -> bad ()
    in
    let result =
      let open Or_error.Let_syntax in
      let%bind project = Program_memory.project requirement in
      match command, get "--source-root", get "--output-dir" with
      | "check", None, None ->
        let%map resolved = Project.elaborate_for_flow project in
        `Assoc
          [ "resources_sexp",
            `String (Sexp.to_string_hum
              ([%sexp_of: Resource.Record.t list]
                 (Elaborated_project.resources resolved.elaborated_project))) ]
      | "emit", Some source_root, Some output_dir ->
        let%map bundle = Project.emit_bundle project ~source_root ~output_dir in
        `Assoc [ "identity", `String (Bundle.identity bundle); "output_dir", `String output_dir ]
      | _ -> bad ()
    in
    (match result with
     | Ok json -> print_endline (Yojson.Safe.pretty_to_string json)
     | Error error ->
       eprintf "%s\n%!" (Error.to_string_hum error);
       Stdlib.exit 1)
  | _ -> bad ()
;;
