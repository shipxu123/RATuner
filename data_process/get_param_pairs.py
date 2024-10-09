# temp = '''| -place_detail_wire_length_opt_effort  + args.detail_wire_length_opt
# | -place_global_clock_gate_aware  + args.global_clock_gate_aware
# | -place_global_clock_power_driven  + false if args.global_clock_power_driven_effort == none else true)
# | -place_global_clock_power_driven_effort  + standard if args.global_clock_power_driven_effort == none else args.global_clock_power_driven_effort
# | -place_global_cong_effort  + args.global_cong_effort
# | -place_global_place_io_pins  + args.global_place_io_pins
# | -place_global_soft_guide_strength  + args.global_soft_guide_strength
# | -place_global_timing_effort  + args.global_timing_effort
# | -place_global_uniform_density  + args.global_uniform_density'''
temp = '''| -drouteUseMultiCutViaEffort + args.post_multicut_via_effort
| -routeWithLithoDriven + args.litho_driven
| -routeWithSiDriven + args.si_driven
| -routeWithTimingDriven + args.timing_driven
| -viaOpt if args.via_opt"
| -wireOpt if args.wire_opt"
| -hold if args.hold'''

commands          = []
processed_options = []

for line in temp.split("\n"):
    if line.find("+") != -1:
        command = line.split("-")[1].split("+")[0]
        options = [i for i in line.split("-")[1].split("+")[1].split("args.")][1:]
    elif line.find("if") != -1:
        command = line.split("-")[1].split("if")[0]
        options = [i for i in line.split("-")[1].split("if")[1].split("args.")][1:]
    else:
        raise NotImplementedError

    processed_option = []
    for option in options:
        if len(option.split()) >= 1:
            processed_option.append(option.split()[0])
        else:
            processed_option.append(option)

    print(command)
    print(processed_option)

    commands.append(command)
    processed_options.append(processed_option)


command_dict = {}

for KS, V in zip(processed_options, commands):
    for K in KS:
        command_dict[K] = V.strip()

print(command_dict)

import json

# with open('placement_param_pairs.json', 'w') as json_file:
#     json.dump(command_dict, json_file, indent=4)

with open('routing_param_pairs.json', 'w') as json_file:
    json.dump(command_dict, json_file, indent=4)