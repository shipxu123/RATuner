import os
import json

# Define the file names
files = [
    'floorplan_command_texts.json',
    'routing_command_texts.json',
    'placement_command_texts.json',
    'synthesis_command_texts.json'
]

# Create a dictionary to store all data
combined_data = {}

# Read and merge data
for file_name in files:
    print(file_name)
    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", file_name), 'r') as file:
        data = json.load(file)
        # Assuming each file contains a dictionary, we merge it into combined_data
        combined_data.update(data)

# Write the merged data into a new JSON file
with open('/home/pxu/codes/RATuner/results/command_texts/command_texts.json', 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print("Files merged successfully, output to '/home/pxu/codes/RATuner/results/command_texts/command_texts.json'")