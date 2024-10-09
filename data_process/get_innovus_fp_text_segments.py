import re

text = """
margin_by enum io die
#######################
-coreMarginsBy {io | die}
Specifies whether the core margins are calculated using the core-to-IO boundary or the core-to-die boundary.
Default: io
Data_type: string, optional
#######################
origin enum llcorner center
#######################
-fplanOrigin {center | llcorner}
Specifies whether the origin of the floorplan should be at the center or at the lower left corner.
Default: llcorner (lower left corner)
Data_type: string, optional
#######################
mode enum r su
#######################
-r {aspectRatio [rowDensity [Left Bottom Right Top]]}
Specifies the chip's core dimensions as the ratio of the height divided by the width. If a value of 1.0 is used, a square chip is defined. A value of 2.0 will define a
rectangular chip with height dimension that is twice the width dimension.

- aspectRatio: Specifies the aspect ratio value.
- rowDensity: Specifies a row density value.
- rowDensity = (std area + block/macro area) / core area
- Left: Specifies the margin from the outside edge of the core box to the left.
- Bottom: Specifies the margin from the outside edge of the core box to the bottom.
- Right: Specifies the margin from the outside edge of the core box to the right.
Top: Specifies the margin from the outside edge of the core box to the top.

The following command creates floorplan by specifying the core dimensions aspect ratio of 1.0,row density of 0.5,and the spacing between core edge to each io box edge of 300.
floorPlan -site tsm3site -r {1.0 0.5 300 300 300 300} -coreMarginsBy io
#######################
-su {aspectRatio [stdCellDensity [Left Bottom Right Top]]}
Determines the core and module sizes by standard cell density.

- aspectRatio: Specifies the aspect ratio value.
- stdCellDensity: Specifies a standard cell density value.
- stdCellDensity =  std cell area/(core area - block/macro area)
- Left: Specifies the margin from the outside edge of the core box to the left.
- Bottom: Specifies the margin from the outside edge of the core box to the bottom.
- Right: Specifies the margin from the outside edge of the core box to the right.
- Top: Specifies the margin from the outside edge of the core box to the top.

The following command creates floorplan by specifying the core dimensions aspect ratio of 1.0,standard cell density of 0.5,and the spacing between core edge to each io box edge of 300.
floorPlan -su {1.0 0.5 300 300 300 300}

Data_type: list, required
#######################
aspect float 0.5 1.0
#######################
- aspectRatio: Specifies the aspect ratio value.
- stdCellDensity: Specifies a standard cell density value.
#######################
density float 0.5 1.0
#######################
- rowDensity = (std area + block/macro area) / core area
#######################
margin float 1.0 5.0
#######################
- Left: Specifies the margin from the outside edge of the core box to the left.
- Bottom: Specifies the margin from the outside edge of the core box to the bottom.
- Right: Specifies the margin from the outside edge of the core box to the right.
- Top: Specifies the margin from the outside edge of the core box to the top.
#######################
make_path_groups enum true false
#######################
# Reset all existing path groups, including basic path groups

reset_path_group -all

# Reset all options set on all path groups

resetPathGroupOptions

# Create collection for each category

set inputs   [all_inputs -no_clocks]
set outputs  [all_outputs]
set icgs     [filter_collection [all_registers] "is_integrated_clock_gating_cell == true"]
set regs     [remove_from_collection [all_registers -edge_triggered] $icgs]
set allregs  [all_registers]

# Create collection for all macros

set blocks      [ dbGet top.insts.cell.baseClass block -p2 ]
set macro_refs  [ list ]
set macros      [ list ]

# If the list of blocks is non-empty, filter out non-physical blocks

set blocks_exist  [ expr [ lindex $blocks 0 ] != 0 ]

if { $blocks_exist } {
  foreach b $blocks {
    set cell    [ dbGet $b.cell ]
    set isBlock [ dbIsCellBlock $cell ]
    set isPhys  [ dbGet $b.isPhysOnly ]
    # Return all blocks that are _not_ physical-only (e.g., filter out IO bondpads)
    if { [ expr $isBlock && ! $isPhys ] } {
      puts [ dbGet $b.name ]
      lappend macro_refs $b
      lappend macros     [ dbGet $b.name ]
    }
  }
}

# Group paths (for any groups that exist)

group_path -name In2Out -from $inputs -to $outputs

if { $allregs != "" } {
  group_path -name In2Reg  -from $inputs  -to $allregs
  group_path -name Reg2Out -from $allregs -to $outputs
}

if { $regs != "" } {
  group_path -name Reg2Reg -from $regs -to $regs
}

if { $allregs != "" && $icgs != "" } {
  group_path -name Reg2ClkGate -from $allregs -to $icgs
}

if { $macros != "" } {
  group_path -name All2Macro -to   $macros
  group_path -name Macro2All -from $macros
}

# High-effort path groups

if { $macros != "" } {
  setPathGroupOptions All2Macro -effortLevel high
  setPathGroupOptions Macro2All -effortLevel high
}

if { $regs != "" } {
  setPathGroupOptions Reg2Reg -effortLevel high
}
#######################
"""

# 正则表达式匹配模式
pattern = re.compile(r"(.*?)\n#{23}\n(.*?)\n#{23}", re.DOTALL)

# 找到所有匹配的模式
matches = pattern.findall(text)

# 创建字典
floorplan_command_dict = {}
for match in matches:
    command, explanation = match
    floorplan_command_dict[command.strip()] = explanation.strip()

# 打印结果
for command, explanation in floorplan_command_dict.items():
    print(f"Command: {command}\nExplanation: {explanation}\n")

import json
with open('/home/pxu/codes/RATuner/results/command_texts/floorplan_command_texts.json', 'w') as json_file:
    json.dump(floorplan_command_dict, json_file, indent=4)