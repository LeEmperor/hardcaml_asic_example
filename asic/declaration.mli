open Core

val create : unit -> Hardcaml_asic.Project.t Or_error.t

(** Explicit consumer generation inputs, relative to the emitter's source root.
    Includes metadata and the emitter itself; no copied dependency sources. *)
val source_inputs : string list
