module U = Unix
open! Core
open Hardcaml_asic

let usage = "Usage: project describe | emit | preflight | run [OPTIONS]"
let bad message = raise (Stdlib.Arg.Bad (message ^ "\n" ^ usage))
(* Executable paths must retain symlink-parent/.. traversal and venv aliases. *)
let anchor_executable path =
  if Filename.is_relative path then Filename.concat (U.getcwd ()) path else path
;;

let absolute path =
  (* Keep kernel traversal across symlink parents, including for missing outputs. *)
  anchor_executable path
;;

let is_file path = try match (U.stat path).st_kind with U.S_REG -> true | _ -> false with _ -> false
let generated path = List.exists (String.split path ~on:'/') ~f:(fun p ->
  List.mem [ "_build"; "_flow_results"; ".dev" ] p ~equal:String.equal)

let check_provider provider =
  let channel = U.open_process_args_in provider [|provider; "--version"; "--json"|] in
  let metadata = Exn.protect ~f:(fun () -> Yojson.Safe.from_channel channel)
    ~finally:(fun () -> match U.close_process_in channel with
      | U.WEXITED 0 -> () | _ -> failwith "Provider --version --json failed; CLI contract 2 is required") in
  let open Yojson.Safe.Util in
  if not (Poly.equal (metadata |> member "cli_contract" |> member "version") (`Int 2)) then
    failwith "Installed hardcaml-asic-flow requires CLI contract 2; install/activate a compatible provider"
;;

let discover () =
  let cwd = U.realpath (U.getcwd ()) in
  if generated cwd then bad "Automatic root discovery is refused in generated trees; use --project-root";
  let rec up path =
    if is_file (Filename.concat path "dune-project")
       && is_file (Filename.concat path "asic-dependency.json") then path
    else let parent = Filename.dirname path in
      if String.equal parent path then bad "No project root found; use --project-root or --source-root"
      else up parent
  in up cwd
;;

let main command args =
  let json = ref false and verbose = ref false and native = ref false in
  let source = ref None and root = ref None and results = ref None and output = ref None in
  let bundle = ref None and tools = ref None and stage = ref None and runs = ref None in
  let python = ref None and support = ref None and pdk = ref None in
  let opt name dest help = name, Stdlib.Arg.String (fun s ->
    if String.is_empty s || String.is_prefix s ~prefix:"--" then bad (name ^ " requires a nonempty path");
    dest := Some s), "PATH " ^ help in
  let common =
    [ "--json", Stdlib.Arg.Set json, " Machine-readable output"
    ; "--verbose", Stdlib.Arg.Set verbose, " Extra diagnostics on stderr" ] in
  let roots = [opt "--source-root" source "Source checkout"; opt "--project-root" root "Project root alias";
               opt "--results-root" results "Results root (default ROOT/_flow_results)"] in
  let routing = [opt "--bundle" bundle "Existing bundle"; opt "--toolchain" tools "Tool root";
    opt "--python" python "Python override"; opt "--support-tools" support "Support tools override";
    opt "--pdk-root" pdk "PDK override"; "--native", Stdlib.Arg.Set native, " Native execution"] in
  let options = match command with
    | "describe" -> common
    | "emit" -> common @ roots @ [opt "--output-dir" output "Exact new or empty bundle directory"]
    | "preflight" -> common @ roots @ routing @ [opt "--output" output "Exact report file"]
    | "run" -> common @ roots @ routing @
      [ "--stage", Stdlib.Arg.String (fun s -> stage := Some s), "synthesis|full Required implementation stage";
        opt "--runs" runs "Run store override" ]
    | _ -> bad "Unknown command" in
  Stdlib.Arg.parse_argv ~current:(ref 0) (Array.of_list (("project " ^ command) :: args))
    options (fun arg -> bad ("Unexpected argument: " ^ arg)) usage;
  if String.equal command "run" then
    (match !stage with Some ("synthesis" | "full") -> () | _ -> bad "run requires --stage synthesis|full");
  let explicit = match !root, !source with
    | Some a, Some b when not (String.equal (U.realpath (absolute a)) (U.realpath (absolute b))) -> bad "Conflicting --project-root and --source-root"
    | Some a, _ | _, Some a -> Some (absolute a) | _ -> None in
  let project = Fifo_asic.project () |> Or_error.ok_exn in
  if String.equal command "describe" then (
    let declaration = Sexp.to_string_hum (Project.describe project) in
    if !json then printf "%s\n%!" (Yojson.Safe.to_string (`Assoc
       [ "project_name", `String (Project.name project); "declaration_sexp", `String declaration ]))
    else printf "%s\n%!" declaration;
    if !verbose then eprintf "Local declaration; not a Workbench protocol payload.\n%!")
  else (
    let root = Option.value_or_thunk explicit ~default:discover in
    let results = Option.value_map !results ~default:(Filename.concat root "_flow_results") ~f:absolute in
    let provider = if List.mem ["preflight"; "run"] command ~equal:String.equal then (
      let paths = String.split (Option.value (Sys.getenv "PATH") ~default:"") ~on:':' in
      match List.find_map paths ~f:(fun dir ->
        let path = anchor_executable (Filename.concat (if String.is_empty dir then "." else dir) "hardcaml-asic-flow") in
        try U.access path [U.X_OK]; if is_file path then Some path else None with _ -> None) with
      | Some path -> check_provider path; Some path
      | None -> failwith "hardcaml-asic-flow is not on PATH; install/activate a compatible provider (CLI contract 2).") else None in
    let emit () =
      if Option.is_none explicit then List.iter (Project.source_inputs project) ~f:(fun input ->
        let path = Filename.concat root input in
        if not (is_file path) || not (String.is_prefix (U.realpath path) ~prefix:(root ^ "/"))
        then bad ("Discovered root lacks expected source input: " ^ input));
      match !output with
      | Some dir when String.equal command "emit" ->
        let dir = absolute dir in
        let b = Project.emit_bundle project ~source_root:root ~output_dir:dir |> Or_error.ok_exn in
        b, dir, false
      | _ ->
        let b, publication = Project.emit_bundle_to_store project ~source_root:root
          ~store_dir:(Filename.concat results "bundles") |> Or_error.ok_exn in
        b, publication.directory, publication.reused in
    if String.equal command "emit" then (
      let b, dir, reused = emit () in
      if !json then printf "%s\n%!" (Yojson.Safe.to_string (`Assoc
        [ "identity", `String (Bundle.identity b); "output_dir", `String dir ]))
      else printf "%s bundle %s\nIdentity: %s\n%!" (if reused then "Reused" else "Created") dir (Bundle.identity b);
      if !verbose then eprintf "Source root: %s\nResults root: %s\n%!" root results)
    else (
      let dir = match !bundle with Some path -> absolute path | None -> let _, dir, _ = emit () in dir in
      let toolchain = Option.first_some !tools (Sys.getenv "TOOLCHAIN" |> Option.filter ~f:(fun s -> not (String.is_empty s)))
        |> Option.value_map ~default:(Filename.concat root "_flow_tools") ~f:absolute in
      let argv = [command; dir; "--results-root"; results; "--toolchain"; toolchain] in
      let argv = List.fold ["--python", !python; "--support-tools", !support; "--pdk-root", !pdk;
        "--output", !output; "--runs", !runs] ~init:argv ~f:(fun a (flag, v) ->
           match v with None -> a | Some p ->
             let path = if String.equal flag "--python" then anchor_executable p else absolute p in
             a @ [flag; path]) in
      let argv = argv @ (Option.value_map !stage ~default:[] ~f:(fun s -> ["--stage"; s]))
        @ (if !native then ["--native"] else []) @ (if !json then ["--json"] else [])
        @ (if !verbose then ["--verbose"] else []) in
      let provider = Option.value_exn provider in
      if !verbose then eprintf "Dispatching installed provider %s (requires CLI contract 2)\n%!" provider;
      U.execv provider (Array.of_list (provider :: argv))))
;;

let () =
  try match Sys.get_argv () |> Array.to_list with
    | [_; ("--help" | "-help")] -> printf "%s\n%!" usage
    | _ :: command :: args -> main command args
    | _ -> bad "A subcommand is required"
  with
  | Stdlib.Arg.Bad message -> eprintf "%s\n%!" message; Stdlib.exit 2
  | Stdlib.Arg.Help message -> printf "%s%!" message
  | exn -> eprintf "project failed: %s\nUse a committed source checkout with the declared inputs and a compatible installed provider (CLI contract 2).\n%!" (Exn.to_string exn); Stdlib.exit 1
