open! Core
open Hardcaml_asic

(* Explicit inventory: declaration discovery itself never reads these files. *)
let source_inputs =
  [ "asic/flow_profiles.ml"; "asic/flow_profiles.mli"
  ; "asic/flow_catalog.ml"; "asic/flow_catalog.mli"
  ]
;;

let create () =
  let open Or_error.Let_syntax in
  let%bind methodology =
    Flow.Methodology.create ~id:"standard" ~label:"Standard"
      ~description:"Fresh LibreLane classic physical-stage prefixes"
      ~backend_recipe:Librelane_classic_v1 ~endpoints:Flow.Stage.all
      ~configurable:Flow.Parameter.Key.all ~defaults:[]
  in
  let%bind profiles = Flow_profiles.create () in
  let%bind entry = Flow.Catalog.Entry.create ~methodology ~profiles ~default_profile:"balanced" in
  Flow.Catalog.create ~entries:[ entry ] ~default_flow:"standard" ~default_profile:"balanced"
;;
