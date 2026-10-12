open! Core
open Hardcaml_asic

let emit ~source_root ~output_dir =
  let open Or_error.Let_syntax in
  let%bind project = Fifo_asic.Declaration.create () in
  let%bind resolved = Project.elaborate_for_flow project in
  let%bind simulation_project = Project.elaborate project ~mode:Simulation in
  let%bind bundle =
    Bundle.render
      ~simulation_project
      ~source_root
      ~input_paths:Fifo_asic.Declaration.source_inputs
      resolved
  in
  let%map () = Bundle.write bundle ~output_dir in
  printf
    "%s\n%!"
    (Yojson.Safe.to_string
       (`Assoc
         [ "identity", `String (Bundle.identity bundle)
         ; "output_dir", `String output_dir
         ]))
;;

let () =
  let source_root = ref None in
  let output_dir = ref None in
  let usage = "emit_bundle --source-root SOURCE_ROOT --output-dir OUTPUT_DIR" in
  Stdlib.Arg.parse
    [ "--source-root", Stdlib.Arg.String (fun s -> source_root := Some s), "PATH Consumer source checkout"
    ; "--output-dir", Stdlib.Arg.String (fun s -> output_dir := Some s), "PATH New or empty bundle directory"
    ]
    (fun arg -> raise (Stdlib.Arg.Bad ("Unexpected argument: " ^ arg)))
    usage;
  match !source_root, !output_dir with
  | Some source_root, Some output_dir ->
    (match Or_error.try_with_join (fun () -> emit ~source_root ~output_dir) with
     | Ok () -> ()
     | Error error ->
       eprintf
         "Bundle emission failed: %s\nSource root must contain the declared inputs and belong to a Git checkout with at least one commit; a no-initial-commit checkout cannot supply provenance.\n%!"
         (Error.to_string_hum error);
       Stdlib.exit 1)
  | _ ->
    eprintf "%s\n%!" usage;
    Stdlib.exit 2
;;
