import re

keywords = {
    "detail_wire_length_opt": "place_detail_wire_length_opt_effort",
    "global_clock_gate_aware": "place_global_clock_gate_aware",
    "global_clock_power_driven_effort": "place_global_clock_power_driven_effort",
    "global_cong_effort": "place_global_cong_effort",
    "global_place_io_pins": "place_global_place_io_pins",
    "global_soft_guide_strength": "place_global_soft_guide_strength",
    "global_timing_effort": "place_global_timing_effort",
    "global_uniform_density": "place_global_uniform_density"
}

# keywords = {
#     "post_multicut_via_effort": "drouteUseMultiCutViaEffort",
#     "litho_driven": "routeWithLithoDriven",
#     "si_driven": "routeWithSiDriven",
#     "timing_driven": "routeWithTimingDriven",
#     "via_opt": "viaOpt",
#     "wire_opt": "wireOpt",
#     "hold": "hold"
# }

matched_lines = []

# 读取文件
with open('/home/pxu/codes/RATuner/results/original_data/innovusTCR.md', 'r') as file:
    lines = file.readlines()

# 定义一个函数来获取前后20行
def get_surrounding_lines(lines, index):
    start = max(0, index)
    end = min(len(lines), index + 21)
    return lines[start:index] + [lines[index]] + lines[index+1:end]

# 遍历字典中的每个键值对
for key, value in keywords.items():
    # 编译正则表达式以匹配行
    pattern = re.compile(re.escape('-'+value))
    
    # 遍历文件的每一行
    for i, line in enumerate(lines):
        if pattern.search(line):
            # 获取匹配行及其前后20行
            surrounding_lines = get_surrounding_lines(lines, i)
            # 将结果添加到数组中
            matched_lines.append((key, surrounding_lines))

# 打印结果
placement_command_text_dict = {}

for k, lines in matched_lines:
    placement_command_text_dict[k] = ''.join(lines)

import json
with open('/home/pxu/codes/RATuner/results/command_texts/placement_command_texts.json', 'w') as json_file:
    json.dump(placement_command_text_dict, json_file, indent=4)

# with open('/home/pxu/codes/RATuner/results/command_texts/routing_command_texts.json', 'w') as json_file:
#     json.dump(placement_command_text_dict, json_file, indent=4)