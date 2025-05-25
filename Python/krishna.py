import os
import subprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Sample training data: (command, intent, name)
data = [
    ("make a folder xyz", "create_folder", "xyz"),
    ("rename file old.txt to new.txt", "rename_file", "old.txt to new.txt"),
    ("rename folder oldfolder to newfolder", "rename_folder", "oldfolder to newfolder"),
    ("create new folder project", "create_folder", "project"),
    ("add a file notes.txt", "create_file", "notes.txt"),
    ("create file test.py", "create_file", "test.py"),
    ("delete folder old_project", "delete_folder", "old_project"),
    ("remove file trash.py", "delete_file", "trash.py"),
    ("erase folder backup", "delete_folder", "backup"),
    ("need a new folder f1/f2", "create_folder", "f1/f2"),
    ("need a new file mydoc.txt", "create_file", "mydoc.txt"),
    ("make a folder named xyz abc", "create_folder", "xyz abc"),
    ("delete file named creative stuff.txt", "delete_file", "creative stuff.txt"),
    ("create folder named delete these", "create_folder", "delete these"),
    ("delete folder named create jobs", "delete_folder", "create jobs"),
    ("create file named stuff.py", "create_file", "stuff.py"),
]

# Split into inputs and labels
commands = [item[0] for item in data]
intents = [item[1] for item in data]

# Train intent classification model
intent_model = make_pipeline(CountVectorizer(ngram_range=(1, 3)), LogisticRegression())
intent_model.fit(commands, intents)

# Simple extractor for file/folder names
def extract_name(command):
    # For rename, extract both old and new names
    if " to " in command:
        parts = command.split(" to ")
        before = parts[0].split()[-1]
        after = parts[1].strip()
        return before + " to " + after

    keywords = ["named", "name", "folder", "file"]
    tokens = command.split()

    for kw in ["named", "name"]:
        if kw in tokens:
            idx = tokens.index(kw)
            return " ".join(tokens[idx + 1:])
    
    for kw in ["folder", "file"]:
        if kw in tokens:
            idx = tokens.index(kw)
            return " ".join(tokens[idx + 1:])
    
    return " ".join(tokens[-2:]) if len(tokens) >= 2 else tokens[-1]

# Perform action
def to_do_commands(intent, name):
    if intent == "create_folder":
        os.makedirs(name, exist_ok=True)
        print(f"✅ Folder '{name}' created.")
    elif intent == "create_file":
        parent_dir = os.path.dirname(name)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        open(name, 'w').close()
        print(f"✅ File '{name}' created.")
    elif intent == "delete_folder":
        try:
            if os.name == 'nt':
                subprocess.run(["rmdir", "/s", "/q", name], shell=True, check=True)
            else:
                subprocess.run(["rm", "-r", name], check=True)
            print(f"🗑️ Folder '{name}' deleted.")
        except Exception as e:
            print(f"❌ Could not delete folder '{name}': {e}")
    elif intent == "delete_file":
        try:
            if os.name == 'nt':
                subprocess.run(["del", name], shell=True, check=True)
            else:
                subprocess.run(["rm", name], check=True)
            print(f"🗑️ File '{name}' deleted.")
        except Exception as e:
            print(f"❌ Could not delete file '{name}': {e}")
    elif intent == "rename_file" or intent == "rename_folder":
        try:
            old_name, new_name = [n.strip() for n in name.split(" to ")]
            os.rename(old_name, new_name)
            print(f"🔄 Renamed '{old_name}' to '{new_name}'.")
        except Exception as e:
            print(f"❌ Could not rename: {e}")

# Basic shell commands allowed
command_list = ["cd", "ls", "mkdir", "echo", "touch", "cat", "dir", "type"]

# Terminal loop
while True:
    print("$ ", end="")
    command = input().strip()

    if command.lower() == "quit":
        break

    if command.startswith("do"):
        intent = intent_model.predict([command])[0]
        name = extract_name(command)
        to_do_commands(intent, name)
    elif command.split(" ")[0] in command_list:
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            print(f"⚠️ Command error: {e}")
    else:
        print("❓ Unknown command. Try using 'do create file xyz.txt' or 'do delete folder abc'")