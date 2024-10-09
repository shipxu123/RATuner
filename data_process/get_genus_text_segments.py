
import re
import json
from collections import OrderedDict
 
# c ='{"b":1, "a":2}'
 
# c = json.loads(c, object_pairs_hook=OrderedDict)
 
# for key in c:
#     print key

with open("/home/pxu/codes/RATuner/results/dependent_tree/genus.txt", "r") as file:
    existing_commands = set([line.rstrip() for line in file.readlines()])


def extract_commands_and_explanations(text):
    # 定义正则表达式模式
    command_pattern = r"\*\*(.*?)\*\*(.*?)(?=\*\*|)"
    # explanation_pattern = r"^(?!\*\*)(.*)$"

    # 用于存储命令和解释的字典
    commands = OrderedDict()

    # 使用正则表达式找到所有命令
    # commands_matches = re.finditer(command_pattern, text, re.DOTALL)

    count = 0
    explanation_text = []

    # for command_match in commands_matches:
    for line in text.split("\n"):
        command_match = re.search(command_pattern, line)

        if command_match:
            match_str = command_match.group().strip("*")

            if "_" in match_str and count % 2 == 0:
                explanation_text = []
                count += 1
                command = match_str
            elif "_" in match_str and count % 2 == 1:
                count += 1
                if command in existing_commands:
                    commands[command] = explanation_text

                command = match_str
                explanation_text = []
                count += 1
            else:
                explanation_text.append(line)
        else:
            explanation_text.append(line)

    commands = {k: "\n".join(v) for k, v in commands.items()}

    return commands

with open("/home/pxu/codes/RATuner/data_process/genus_attref_legacy.md", "r") as file:
    text = file.read()

commands_info = extract_commands_and_explanations(text)
# for command, explanation in commands_info.items():
#     print("-" * 40)
#     print(f"Command: {command}")
#     print(f"Explanation: {explanation}")
#     print("-" * 40)
#     print()


extracted_commands = set(commands_info.keys())


# print( extracted_commands.intersection(existing_commands)  )
print(existing_commands.difference(extracted_commands))
# print(existing_commands)

# print(len(commands_info.keys()))

import json
with open('/home/pxu/codes/RATuner/results/command_texts/synthesis_command_texts.json', 'w') as json_file:
    json.dump(commands_info, json_file, indent=4)