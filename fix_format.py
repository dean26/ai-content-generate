import json

# Read the JSONL file
with open('result.jsonl', 'r') as file:
    lines = file.readlines()

# Process each line
modified_lines = []
for line in lines:
    data = json.loads(line)
    content = data["messages"][2]["content"]
    article_length = len(content)
    user_message = data["messages"][1]["content"]
    new_user_message = user_message.replace("The article should include the keywords", f"The article should be about {article_length} characters long and include the keywords:")
    data["messages"][1]["content"] = new_user_message
    modified_lines.append(json.dumps(data))

# Write the modified content back to the file
with open('results_modified.jsonl', 'w') as file:
    for modified_line in modified_lines:
        file.write(modified_line + '\n')

print("File has been modified and saved as 'results_modified.jsonl'.")
