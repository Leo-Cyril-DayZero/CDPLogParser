import re
import json
import glob

directory = input("Enter the directory containing the log files: ")
log_files = glob.glob(directory+"/*.log")

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
pattern2 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+) (\w+/\w+/\w+/\w+): (.*)"
pattern3 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (\w+[\w\s]+) ([\w\/]+): (.*)"
pattern4 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) \[(\d+)\] \[(\w+)\] (.*)"
pattern5 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+): (\w+): (\w+)"

patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]

# Open the log file
for log_file in log_files:
    with open(log_file, "r") as f:
        # Read each line of the file
        for line in f:
            match = None
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    break
            if match:
                log_entry = {
                    "date_time": match.group(1),
                    "thread_id": match.group(2),
                    "log_level": match.group(3),
                    "subsystem":"N/A",
                    "component":"N/A",
                    "action":"N/A",
                    "message":"N/A",
                }
                if pattern == pattern4:
                    log_entry["message"] = match.group(4)
                else:
                    log_entry["subsystem"] = match.group(4)
                if len(match.groups()) >= 5:
                    log_entry["component"] = match.group(5)
                if len(match.groups()) >= 6: 
                    log_entry["action"] = match.group(6)
                if len(match.groups()) >= 7:
                    log_entry["message"] = match.group(7)
                if pattern == pattern1:
                    log_entry["Pattern"] = "Pattern1"
                if pattern == pattern2:
                    log_entry["Pattern"] = "Pattern2"
                if pattern == pattern3:
                    log_entry["Pattern"] = "Pattern3"
                if pattern == pattern4:
                    log_entry["Pattern"] = "Pattern4"
                if pattern == pattern5:
                    log_entry["Pattern"] = "Pattern4"
                
                log_entries.append(log_entry)
            else:
                unmatched_entries.append(line)


output_string = ""
output_string += "[\n"
for entry in log_entries:
    output_string += "\n"
    output_string += json.dumps(entry, indent=4)
    output_string += ","
output_string += "}"
output_string += "]"

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

