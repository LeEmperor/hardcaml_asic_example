open! Core
open Hardcaml_asic

let emit ~source_root ~output_dir =
  let open Or_error.Let_syntax in
  let%bind project = Fifo_asic.project () in
  let%map bundle = Hardcaml_asic.Project.emit_bundle project ~source_root ~output_dir in
  printf
    "%s\n%!"
    (Yojson.Safe.to_string
       (`Assoc
         [ "identity", `String (Bundle.identity bundle)
         ; "output_dir", `String output_dir
         ]))
;;

let emit_args argv =
  let source_root = ref None in
  let output_dir = ref None in
  let usage = "project emit --source-root SOURCE_ROOT --output-dir OUTPUT_DIR" in
  Stdlib.Arg.parse_argv ~current:(ref 0) argv
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

let usage = "Usage: project describe | project emit --source-root ROOT --output-dir DIR"

let () =
  try
    match Sys.get_argv () |> Array.to_list with
    | [ _; ("--help" | "-help") ] -> printf "%s\n%!" usage
    | [ _; "describe" ] ->
      (match Fifo_asic.project () with
       | Ok project -> printf "%s\n%!" (Sexp.to_string_hum (Hardcaml_asic.Project.describe project))
       | Error error ->
         eprintf "%s\n%!" (Error.to_string_hum error);
         Stdlib.exit 1)
    | _ :: "emit" :: args -> emit_args (Array.of_list ("project emit" :: args))
    | _ ->
      eprintf "%s\n%!" usage;
      Stdlib.exit 2
  with
  | Stdlib.Arg.Bad message ->
    eprintf "%s\n%!" message;
    Stdlib.exit 2
  | Stdlib.Arg.Help message -> printf "%s%!" message
;;
