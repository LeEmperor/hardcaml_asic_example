drc off
crashbackups disable
locking disable
lef read {/home/wayne/devel/jane/hardcaml_asic_example/_flow_tools/pdk/ihp-sg13cmos5l/libs.ref/sg13cmos5l_stdcell/lef/sg13cmos5l_tech.lef}
lef read {/home/wayne/devel/jane/hardcaml_asic_example/_flow_tools/pdk/ihp-sg13cmos5l/libs.ref/sg13cmos5l_stdcell/lef/sg13cmos5l_stdcell.lef}
lef read {/home/wayne/devel/jane/hardcaml_asic_example/_flow_tools/pdk/ihp-sg13cmos5l/libs.ref/sg13cmos5l_sram/lef/RM_IHPSG13_1P_256x16_c2_bm_bist.lef}
set ::env(STEP_DIR) {/home/wayne/devel/jane/hardcaml_asic_example/_flow_results/sram-physical/runs/20261025T034710180883Z_be961b2c/project/runs/asic/magic-stock-abstract-baseline}
set ::env(DESIGN_NAME) {RM_IHPSG13_1P_256x16_c2_bm_bist}
set report_dir $::env(STEP_DIR)/reports

set drc_rpt_path $report_dir/drc.magic.rpt
set fout [open $drc_rpt_path w]
set oscale [cif scale out]
set cell_name $::env(DESIGN_NAME)
magic::suspendall
puts stdout "\[INFO\] Loading $cell_name\n"
flush stdout
load $cell_name
select top cell
drc euclidean on
drc style drc(full)
drc check
set drcresult [drc listall why]


set count 0
puts $fout "$cell_name"
puts $fout "----------------------------------------"
foreach {errtype coordlist} $drcresult {
    puts $fout $errtype
    puts $fout "----------------------------------------"
    foreach coord $coordlist {
        set bllx [expr {$oscale * [lindex $coord 0]}]
        set blly [expr {$oscale * [lindex $coord 1]}]
        set burx [expr {$oscale * [lindex $coord 2]}]
        set bury [expr {$oscale * [lindex $coord 3]}]
        set coords [format " %.3fum %.3fum %.3fum %.3fum" $bllx $blly $burx $bury]
        puts $fout "$coords"
        set count [expr {$count + 1} ]
    }
    puts $fout "----------------------------------------"
}

puts $fout "\[INFO\] COUNT: $count"
puts $fout "\[INFO\] Should be divided by 3 or 4"

puts $fout ""
close $fout

puts stdout "\[INFO\] COUNT: $count"
puts stdout "\[INFO\] Should be divided by 3 or 4"
puts stdout "\[INFO\] DRC Checking DONE ($drc_rpt_path)"
flush stdout

set views_dir $::env(STEP_DIR)/views
file mkdir $views_dir

set mag_view $views_dir/$::env(DESIGN_NAME).drc.mag
puts stdout "\[INFO\] Saving mag view with DRC errors ($mag_view)"
# WARNING: changes the name of the cell; keep as last step
save $mag_view
puts stdout "\[INFO\] Saved"

quit -noprompt
