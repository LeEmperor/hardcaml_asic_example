(* Acceptance consumer of installed public APIs; no local reconciliation engine. *)
open Hardcaml_asic_execution

let () =
  let operation = Sys.argv.(1) and path = Sys.argv.(2) in
  let read () = Evidence_json.value (Evidence_json.read path) in
  let verdict = function
    | Ok _ -> `Assoc [ "valid", `Bool true ]
    | Error reason -> `Assoc [ "valid", `Bool false; "reason", `String reason ]
  in
  let result =
    match operation with
    | "inspect" ->
      (match Resource_evidence.inspect ~run_dir:path with
       | Ok evidence -> evidence
       | Error reason -> invalid_arg reason)
    | "validate" -> verdict (Resource_evidence.validate (read ()))
    | "verify-sources" ->
      verdict (Resource_evidence.verify_sources ~run_dir:Sys.argv.(3) (read ()))
    | "collect" -> Collect_service.to_json (Collect_service.collect path)
    | "report" ->
      let report = Report_service.run path in
      `Assoc
        [ "accepted", `Bool (Report_service.accepted report.verdict)
        ; "problems", `List (List.map (fun s -> `String s) report.verdict.problems)
        ; "results", report.results
        ]
    | "archive-sources" ->
      let archive = Archive_service.inspect ~run_dir:path in
      `List (List.map (fun (source : Evidence_tar.source) -> `String source.name) archive.reports)
    | _ -> invalid_arg "unsupported acceptance operation"
  in
  print_endline (Yojson.Safe.to_string result)
