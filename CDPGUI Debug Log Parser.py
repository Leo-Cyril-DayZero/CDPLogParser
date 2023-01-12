
import re
import json

# The log file to parse
log_file = "2022-11-30_100341_Debug.log"

# The output json file
json_file = "output.json"

# A list to hold the parsed log entries
log_entries = []

# Define the patterns for the different log formats
pattern1 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+[\w\s]+) ([\w\/]+): (\w+[\w\s]+): ([\w-]+)"
pattern2 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+): (\w+): (\w+)"

# Open the log file
with open(log_file, "r") as f:
    # Read each line of the file
    for line in f:
        match1 = re.match(pattern1, line)
        if match1:
            log_entry = {
                "date_time": match1.group(1),
                "thread_id": match1.group(2),
                "log_level": match1.group(3),
                "subsystem": match1.group(4),
                "component": match1.group(5),
                "action": match1.group(6),
                "guid": match1.group(7)
            }
            log_entries.append(log_entry)
        else:
            match2 = re.match(pattern2, line)
            if match2:
                log_entry = {
                    "date_time": match2.group(1),
                    "subsystem": match2.group(2),
                    "component": match2.group(3),
                    "action": match2.group(4),
                }
                log_entries.append(log_entry)

output_string = ""
for entry in log_entries:
    output_string += "{\n"
    output_string += json.dumps(entry, indent=4)
    output_string += "\n},\n"

output_string = output_string[:-2]  # remove the trailing comma and newline

# Open the output json file
with open(json_file, "w") as f:
    f.write(output_string)

print("Log entries written to", json_file)
