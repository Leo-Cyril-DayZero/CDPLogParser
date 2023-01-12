
import re
import json

# The log file to parse
log_file = "2022-11-30_100341_Debug.log"

# The output json file
json_file = "output.json"

# The output file for unmatched entries
unmatched_file = "unmatched.log"

# A list to hold the parsed log entries
log_entries = []

# A list to hold the log entries that don't match any of the patterns
unmatched_entries = []

# Define the patterns for the different log formats
pattern1 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+[\w\s]+) ([\w\/]+): (\w+[\w\s]+): (.*)"
pattern2 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+): (\w+): (\w+)"
pattern3 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+[\w\s]+) ([\w\/]+): (.*)"
pattern4 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+[\w\s_]+)"

patterns = [pattern1, pattern2, pattern3, pattern4]

# Open the log file
with open(log_file, "r") as f:
    # Read each line of the file
    for line in f:
        match = None
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                break
        if match:
            #print(pattern)
            log_entry = {
                "date_time": match.group(1),
                "thread_id": match.group(2),
                "log_level": match.group(3),
                #"subsystem": match.group(4),
                # "pattern_used": pattern.__str__()
            }
            if pattern == pattern4:
                log_entry["message"] = match.group(4)
            else:
                log_entry["subsystem"] = match.group(4)
            if len(match.groups()) == 5:
                log_entry["component"] = match.group(5)
                log_entry["action"] = match.group(6)
            if len(match.groups()) == 7:
                log_entry["component"] = match.group(5)
                log_entry["action"] = match.group(6)
                log_entry["guid"] = match.group(7)
            log_entries.append(log_entry)
        else:
            unmatched_entries.append(line)


output_string = ""
for entry in log_entries:
    output_string += "{\n"
    output_string += json.dumps(entry, indent=4)
    output_string += "\n},\n"

output_string = output_string[:-2]  # remove the trailing comma and newline

# Open the output json file
with open(json_file, "w") as f:
    f.write(output_string)

# Open the unmatched log entries file
with open(unmatched_file, "w") as f:
    for line in unmatched_entries:
        f.write(line)

print("Matched Log entries written to", json_file)
print("Unmatched Log entries written to", unmatched_file)

