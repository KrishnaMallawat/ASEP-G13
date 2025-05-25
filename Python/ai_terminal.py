import os
import re
import subprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Static, Input, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical

# Expanded training data for better natural language support
sentences = [
    # Rename file/folder
    "rename file old.txt to new.txt", "rename folder oldfolder to newfolder",
    "rename old.txt to new.txt", "rename oldfolder to newfolder",
    "change file a.txt to b.txt", "change folder a to b",
    "move file a.txt to b.txt", "move folder a to b",
    "rename notes.md as notes_final.md", "switch script.py to script_v2.py",
    "rename backups as backups_archive", "switch music to music_collection",
    # Create file/folder
    "make a folder xyz", "create new folder project", "add a file notes.txt",
    "create file test.py", "new file report.txt", "create a new file called data.csv",
    "make file notes.md", "generate file summary.docx", "add file script.py",
    "new folder images", "create a new folder called docs", "make directory backups",
    "add folder music", "generate folder videos",
    # Delete file/folder
    "delete folder old_project", "remove file trash.py", "erase folder backup",
    "need a new folder", "need a new file", "delete all text files",
    "delete file named creative stuff", "create folder named delete these",
    "delete folder named create jobs", "create file named stuff",
    "remove directory temp", "delete the file called report.docx",
    "make directory logs", "generate a file output.txt", "eliminate folder test_data",
    "remove report.txt", "delete the file data.csv", "erase file notes.md",
    "eliminate script.py", "trash file summary.docx",
    "remove images", "delete the folder docs", "erase folder backups",
    "eliminate directory music", "trash folder videos",
    # List files/folders
    "list all files in current directory", "show me all folders",
    "show files", "show all files", "list files", "display files",
    "show folders", "show all folders", "list folders", "display folders",
    # Undo
    "undo last action", "revert last change", "go back", "undo"
]
labels = [
    # Rename file/folder
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_file",
    "rename_folder", "rename_folder",
    # Create file/folder
    "create_folder", "create_folder", "create_file",
    "create_file", "create_file", "create_file",
    "create_file", "create_file", "create_file",
    "create_folder", "create_folder", "create_folder",
    "create_folder", "create_folder",
    # Delete file/folder
    "delete_folder", "delete_file", "delete_folder",
    "create_folder", "create_file", "delete_file",
    "delete_file", "create_folder", "delete_folder", "create_file",
    "delete_folder", "delete_file", "create_folder", "create_file", "delete_folder",
    "delete_file", "delete_file", "delete_file", "delete_file", "delete_file",
    "delete_folder", "delete_folder", "delete_folder", "delete_folder", "delete_folder",
    # List files/folders
    "list_files", "list_folders",
    "list_files", "list_files", "list_files", "list_files",
    "list_folders", "list_folders", "list_folders", "list_folders",
    # Undo
    "undo", "undo", "undo", "undo"
]

model = make_pipeline(CountVectorizer(ngram_range=(1, 3)), LogisticRegression(max_iter=1000))
model.fit(sentences, labels)
history = []

INSTRUCTIONS = (
    "[b yellow]Supported Commands:[/b yellow]\n"
    "- create/make/add/generate a file/folder named <name>\n"
    "- delete/remove/erase/eliminate a file/folder named <name>\n"
    "- rename/change/move/switch file/folder oldname to newname\n"
    "- list/show/display all files/folders\n"
    "- undo (reverts last create/delete)\n"
    "\n[b yellow]Examples:[/b yellow]\n"
    "  create folder test123\n"
    "  delete file old.txt\n"
    "  rename file old.txt to new.txt\n"
    "  change folder docs to docs_old\n"
    "  show files\n"
    "  undo"
)

def extract_name(command):
    # For rename, extract both old and new names
    if " to " in command:
        parts = command.split(" to ")
        before = parts[0].split()[-1]
        after = parts[1].strip()
        return before + " to " + after
    if " as " in command:
        parts = command.split(" as ")
        before = parts[0].split()[-1]
        after = parts[1].strip()
        return before + " to " + after
    if " switch " in command:
        parts = command.split(" switch ")
        before = parts[0].split()[-1]
        after = parts[1].strip()
        return before + " to " + after
    match = re.search(r"(?:named|called|name)\s+([^\s]+)", command)
    if match:
        return match.group(1)
    match = re.search(r"(?:file|folder|directory)\s+([^\s]+)$", command)
    if match:
        return match.group(1)
    bits = command.strip().split()
    if len(bits) > 2:
        return bits[-1]
    return "unnamed"

def to_do_commands(intent, name):
    try:
        if intent == "create_folder":
            os.makedirs(name, exist_ok=True)
            history.append(('delete_folder', name))
            return f" Folder '{name}' created."
        elif intent == "create_file":
            open(name, 'w').close()
            history.append(('delete_file', name))
            return f" File '{name}' created."
        elif intent == "delete_folder":
            if os.path.isdir(name):
                os.system(f"rm -rf {name}")
                history.append(('create_folder', name))
                return f" Folder '{name}' deleted."
            else:
                return f" Folder '{name}' does not exist."
        elif intent == "delete_file":
            if os.path.isfile(name):
                os.remove(name)
                history.append(('create_file', name))
                return f" File '{name}' deleted."
            else:
                return f" File '{name}' does not exist."
        elif intent == "rename_file" or intent == "rename_folder":
            if " to " in name:
                old_name, new_name = [n.strip() for n in name.split(" to ")]
                if not os.path.exists(old_name):
                    return f" '{old_name}' does not exist."
                os.rename(old_name, new_name)
                return f" Renamed '{old_name}' to '{new_name}'."
            else:
                return " Please use the format: rename file old.txt to new.txt "
        elif intent == "list_files":
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return "[b]Files:[/b]\n" + ("\n".join(files) if files else "[dim]No files found.[/dim]")
        elif intent == "list_folders":
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
            return "[b]Folders:[/b]\n" + ("\n".join(folders) if folders else "[dim]No folders found.[/dim]")
        elif intent == "undo":
            return undo_last()
        else:
            return " Unknown or unsupported intent."
    except Exception as e:
        return f" Error: {str(e)}"

def undo_last():
    if not history:
        return "Nothing to undo."
    last_action, name = history.pop()
    try:
        if last_action == 'delete_folder':
            os.system(f"rm -rf {name}")
            return f" Undo: Folder '{name}' deleted."
        elif last_action == 'delete_file':
            os.remove(name)
            return f" Undo: File '{name}' deleted."
        elif last_action == 'create_folder':
            os.makedirs(name, exist_ok=True)
            return f" Undo: Folder '{name}' re-created."
        elif last_action == 'create_file':
            open(name, 'w').close()
            return f"Undo: File '{name}' re-created."
    except Exception as e:
        return f" Undo failed: {str(e)}"
    return "Undo not supported for this action."

class CommandLogApp(App):
    CSS = """
    Screen { align: center middle; }
    #main { width: 90%; height: 70%; }
    #table-panel { border: round green; padding: 1; height: 100%; }
    #button-panel { border: round red; width: 24; align: center middle; padding: 1; }
    Button { height: 3; min-width: 16; content-align: center middle; }
    #enter-btn { background: #7ed957; color: black !important; border: round #7ed957; }
    TabbedContent { min-height: 10; }
    TabPane { padding: 1; }
    DataTable { height: 100%; }
    #header { content-align: center middle; height: 3; width: 90%; }
    #command_input { width: 90%; border: round blue; margin-bottom: 1; }
    """

    TITLE = "AI Terminal and Command Log"

    def compose(self) -> ComposeResult:
        yield Static(self.TITLE, id="header")
        yield Input(placeholder="Enter command here...", id="command_input")
        with Horizontal(id="main"):
            with Vertical(id="table-panel"):
                with TabbedContent(id="main-tabs"):
                    with TabPane("Instructions", id="help-tab"):
                        yield Static(INSTRUCTIONS, markup=True)
            with Vertical(id="button-panel"):
                yield Button("Enter", id="enter-btn")
    def on_mount(self):
        self.query_one(Input).focus()
        self.query_one(TabbedContent).active = "help-tab"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        input_box = self.query_one(Input)
        tabs = self.query_one("#main-tabs", TabbedContent)
        
        if btn_id == "enter-btn":
            self.handle_command(input_box.value)
            input_box.value = ""
            input_box.focus()
 
            open("command_log.txt", "w").close()


    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.handle_command(event.value)
        event.input.value = ""
        event.input.focus()

    def handle_command(self, command):
        command = command.strip()

        if not command:
            return
        if command.lower() == "help":
            return
        if command.lower() == "undo":
            result = undo_last()
            with open("command_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Command: undo\nResult: {result}\n\n")
            return

        name = extract_name(command)
        intent = model.predict([command])[0]
        result = to_do_commands(intent, name)
        with open("command_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Command: {command}\nResult: {result}\n\n")

if __name__ == "__main__":
    CommandLogApp().run()