import os
import re
import shutil
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Static, Input, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical

# Expanded training data for better natural language support
sentences = [
    # Search in file commands
    "search hello in file.txt", "find error in log.txt", "look for world in notes.md",
    "search for text in file.txt", "find the word hello in test.txt",
    "search 'hello world' in file.txt", "find \"error message\" in log.txt",
    "look up debug in app.log", "search for password in config.txt",
    "find the phrase hello world in doc.txt",
    
    # Rename file/folder
    "rename file old.txt to new.txt", "rename folder oldfolder to newfolder",
    "rename old.txt to new.txt", "rename oldfolder to newfolder",
    "change file a.txt to b.txt", "change folder a to b",
    "move file a.txt to b.txt", "move folder a to b",
    "rename notes.md as notes_final.md", "switch script.py to script_v2.py",
    "rename backups as backups_archive", "switch music to music_collection",
    "rename all .txt files to .md", "rename all .log files to .bak",
    
    # Create file/folder
    "make a folder xyz", "create new folder project", "add a file notes.txt",
    "create file test.py", "new file report.txt", "create a new file called data.csv",
    "make file notes.md", "generate file summary.docx", "add file script.py",
    "new folder images", "create a new folder called docs", "make directory backups",
    "add folder music", "generate folder videos",
    "make fil.txt", "create fil.txt", "add fil.txt", "generate fil.txt", "new fil.txt",
    "make file fil.txt", "create file fil.txt", "add file fil.txt", "generate file fil.txt", "new file fil.txt",
    
    # Delete file/folder
    "delete folder old_project", "remove file trash.py", "erase folder backup",
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
    
    # Disk usage
    "show disk usage", "how much space is left", "display disk usage",
    "check disk space", "show space usage", "display storage info",
    
    # History
    "show history", "display history", "command history",
    "show command log", "display command log", "show previous commands",
    
    # Undo
    "undo last action", "revert last change", "go back", "undo",
    "undo last command", "revert previous action"
]
labels = [
    # Search in file commands
    "search_in_file", "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file",
    
    # Rename file/folder
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_file",
    "rename_folder", "rename_folder",
    "rename_multiple_files", "rename_multiple_files",
    
    # Create file/folder
    "create_folder", "create_folder", "create_file",
    "create_file", "create_file", "create_file",
    "create_file", "create_file", "create_file",
    "create_folder", "create_folder", "create_folder",
    "create_folder", "create_folder",
    "create_file", "create_file", "create_file", "create_file", "create_file",
    "create_file", "create_file", "create_file", "create_file", "create_file",
    
    # Delete file/folder
    "delete_folder", "delete_file", "delete_folder",
    "delete_file", "create_folder",
    "delete_folder", "create_file",
    "delete_folder", "delete_file",
    "create_folder", "create_file", "delete_folder",
    "delete_file", "delete_file", "delete_file",
    "delete_file", "delete_file",
    "delete_folder", "delete_folder", "delete_folder",
    "delete_folder", "delete_folder",
    
    # List files/folders
    "list_files", "list_folders",
    "list_files", "list_files", "list_files", "list_files",
    "list_folders", "list_folders", "list_folders", "list_folders",
    
    # Disk usage
    "disk_usage", "disk_usage", "disk_usage",
    "disk_usage", "disk_usage", "disk_usage",
    
    # History
    "history", "history", "history",
    "history", "history", "history",
    
    # Undo
    "undo", "undo", "undo", "undo",
    "undo", "undo"
]

model = make_pipeline(
    CountVectorizer(ngram_range=(1, 3), analyzer='char_wb'),
    LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')
)
model.fit(sentences, labels)
history = []
command_history = []

INSTRUCTIONS = (
    "[b yellow]Supported Commands (case-insensitive, flexible):[/b yellow]\n"
    "- create/make/add/generate a file/folder named <name>\n"
    "- delete/remove/erase/eliminate a file/folder named <name>\n"
    "- delete all <type> files (e.g., delete all picture files, delete all text files)\n"
    "- rename/change/move/switch file/folder <oldname> to <newname>\n"
    "- rename all <ext1> files to <ext2> (e.g., rename all .txt files to .md)\n"
    "- search/find/look for <text> in <file> (e.g., search hello in notes.txt)\n"
    "- show/display disk usage\n"
    "- show/display command history\n"
    "- list/show/display all files/folders\n"
    "- undo (reverts last create/delete)\n"
    "\n[b yellow]Examples:[/b yellow]\n"
    "  create folder test123\n"
    "  create file data.csv\n"
    "  add a file notes.txt\n"
    "  make directory backups\n"
    "  delete file old.txt\n"
    "  remove folder temp\n"
    "  erase file trash.py\n"
    "  eliminate directory music\n"
    "  rename file old.txt to new.txt\n"
    "  change folder docs to docs_old\n"
    "  move file a.txt to b.txt\n"
    "  switch script.py to script_v2.py\n"
    "  rename all .txt files to .md\n"
    "  search hello in notes.txt\n"
    "  find error in log.txt\n"
    "  look for password in config.txt\n"
    "  show disk usage\n"
    "  show history\n"
    "  display files\n"
    "  list folders\n"
    "  undo\n"
    "\n[b yellow]Tips:[/b yellow]\n"
    "- You can use natural language, e.g., 'please create a new file called data.csv'.\n"
    "- All commands are case-insensitive.\n"
    "- For batch rename, use: rename all .ext1 files to .ext2\n"
    "- For searching, you can use: search/find/look for <text> in <file>\n"
    "- Undo only works for the last create/delete action.\n"
    "- Command log is saved to [b]command_log.txt[/b].\n"
)
def extract_name(command):
    # For delete all type files: "delete all text files"
    match = re.search(r"(?:delete|remove|erase)\s+all\s+(\w+)\s*(?:files)?", command.lower())
    if match:
        return match.group(1)
        
    # For search in file: "search hello in file.txt"
    match = re.search(r"(?:search|find|look for)\s+['\"]?([^'\"]+?)['\"]?\s+in\s+([^\s]+)", command)
    if match:
        return f"{match.group(1)} in {match.group(2)}"
        
    # For rename multiple files: "rename all .txt files to .md"
    match = re.search(r"rename all (\.\w+) files to (\.\w+)", command)
    if match:
        return f"{match.group(1)} to {match.group(2)}"
        
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
    # If command is like "make fil.txt" or "create fil.txt"
    tokens = command.strip().split()
    if len(tokens) >= 2 and "." in tokens[-1]:
        return tokens[-1]
    # fallback
    if len(tokens) > 2:
        return tokens[-1]
    return "unnamed"

def to_do_commands(intent, name):
    try:
        if intent == "create_folder":
            os.makedirs(name, exist_ok=True)
            history.append(('delete_folder', name))
            return f"[green] Folder '{name}' created.[/green]"
        elif intent == "create_file":
            open(name, 'w').close()
            history.append(('delete_file', name))
            return f"[green] File '{name}' created.[/green]"
        elif intent == "delete_folder":
            if os.path.isdir(name):
                shutil.rmtree(name)
                history.append(('create_folder', name))
                return f"[red] Folder '{name}' deleted.[/red]"
            else:
                return f"[yellow] Folder '{name}' does not exist.[/yellow]"
        elif intent == "delete_file":
            if os.path.isfile(name):
                os.remove(name)
                history.append(('create_file', name))
                return f"[red] File '{name}' deleted.[/red]"
            else:
                return f"[yellow] File '{name}' does not exist.[/yellow]"
        elif intent == "rename_file" or intent == "rename_folder":
            if " to " in name:
                old_name, new_name = [n.strip() for n in name.split(" to ")]
                if not os.path.exists(old_name):
                    return f"[yellow] '{old_name}' does not exist.[/yellow]"
                os.rename(old_name, new_name)
                return f"[cyan] Renamed '{old_name}' to '{new_name}'.[/cyan]"
            else:
                return "[yellow] Please use the format: rename file old.txt to new.txt [/yellow]"
        elif intent == "rename_multiple_files":
            try:
                ext_from, ext_to = [s.strip() for s in name.split(" to ")]
                count = 0
                for fname in os.listdir('.'):
                    if fname.endswith(ext_from):
                        new_name = fname[:-len(ext_from)] + ext_to
                        os.rename(fname, new_name)
                        count += 1
                return f"[cyan]Renamed {count} files from {ext_from} to {ext_to}.[/cyan]" if count else f"[yellow]No files with {ext_from} found.[/yellow]"
            except Exception as e:
                return f"[red] Error renaming multiple files: {str(e)}[/red]"
        elif intent == "search_in_file":
            try:
                search_text, filename = [s.strip() for s in name.split(" in ")]
                if not os.path.isfile(filename):
                    return f"[yellow]File '{filename}' does not exist.[/yellow]"
                with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                matches = []
                for i, line in enumerate(lines, 1):
                    if search_text.lower() in line.lower():
                        matches.append(f"Line {i}: {line.strip()}")
                if matches:
                    return "[b]Matches found:[/b]\n" + "\n".join(matches)
                else:
                    return f"[yellow]No matches found for '{search_text}' in '{filename}'.[/yellow]"
            except Exception as e:
                return f"[red]Error searching in file: {str(e)}[/red]"
        elif intent == "disk_usage":
            try:
                total, used, free = shutil.disk_usage(os.getcwd())
                return (f"[b]Disk Usage:[/b]\n"
                        f"Total: {total // (2**20)} MB\n"
                        f"Used: {used // (2**20)} MB\n"
                        f"Free: {free // (2**20)} MB")
            except Exception as e:
                return f"[red] Error getting disk usage: {str(e)}[/red]"
        elif intent == "history":
            if not command_history:
                return "[yellow]No commands in history.[/yellow]"
            return "[b]Command History:[/b]\n" + "\n".join(command_history)
        elif intent == "list_files":
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return "[b]Files:[/b]\n" + ("\n".join(files) if files else "[dim]No files found.[/dim]")
        elif intent == "list_folders":
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
            return "[b]Folders:[/b]\n" + ("\n".join(folders) if folders else "[dim]No folders found.[/dim]")
        elif intent == "undo":
            return undo_last()
        elif intent == "delete_by_type":
            type_map = {
                "picture": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
                "text": [".txt", ".log", ".md"],
                "word": [".doc", ".docx"],
                "document": [".doc", ".docx", ".pdf", ".txt"],
                "pdf": [".pdf"],
                "python": [".py"],
                "video": [".mp4", ".avi", ".mov", ".mkv"],
                "audio": [".mp3", ".wav", ".ogg"]
            }
            
            file_type = name.lower().replace("files", "").replace("all", "").strip()
            if file_type not in type_map:
                return f"[yellow]Unknown file type. Supported types: {', '.join(type_map.keys())}[/yellow]"
            
            extensions = type_map[file_type]
            deleted_files = []
            
            for file in os.listdir('.'):
                if any(file.lower().endswith(ext) for ext in extensions):
                    try:
                        os.remove(file)
                        deleted_files.append(file)
                    except Exception as e:
                        continue
            
            if deleted_files:
                history.append(('restore_files', deleted_files))
                return f"[red]Deleted {len(deleted_files)} {file_type} files: {', '.join(deleted_files)}[/red]"
            return f"[yellow]No {file_type} files found to delete.[/yellow]"
        else:
            return "[magenta] Unknown or unsupported intent.[/magenta]"
    except Exception as e:
        return f"[red] Error: {str(e)}[/red]"


def undo_last():
    if not history:
        return "[yellow]Nothing to undo.[/yellow]"
    last_action, files = history.pop()
    try:
        if last_action == 'delete_folder':
            if os.path.isdir(files):
                shutil.rmtree(files)
                return f"[red] Undo: Folder '{files}' deleted.[/red]"
            else:
                return f"[yellow] Folder '{files}' does not exist for undo.[/yellow]"
        elif last_action == 'delete_file':
            if os.path.isfile(files):
                os.remove(files)
                return f"[red] Undo: File '{files}' deleted.[/red]"
            else:
                return f"[yellow] File '{files}' does not exist for undo.[/yellow]"
        elif last_action == 'create_folder':
            os.makedirs(files, exist_ok=True)
            return f"[green] Undo: Folder '{files}' re-created.[/green]"
        elif last_action == 'create_file':
            open(files, 'w').close()
            return f"[green] Undo: File '{files}' re-created.[/green]"
        elif last_action == 'restore_files':
            for file in files:
                open(file, 'w').close()
            return f"[green]Restored {len(files)} files: {', '.join(files)}[/green]"
    except Exception as e:
        return f"[red] Undo failed: {str(e)}[/red]"
    return "[yellow]Undo not supported for this action.[/yellow]"

def predict_intent(command):
    # Special case for deleting files by type
    if re.search(r"(?:delete|remove|erase)\s+(?:all\s+)?(?:picture|text|word|image|document|pdf|python|video|audio)(?:\s+files)?", command.lower()):
        return "delete_by_type"
    # Special case for search commands
    if any(command.lower().startswith(x) for x in ['search', 'find', 'look for']):
        return 'search_in_file'
    return model.predict([command])[0]

class CommandLogApp(App):
    CSS = """
    Screen { align: center middle; }
    #main { width: 90%; height: 90%; }
    #table-panel { border: round green; padding: 1; height: 100%; }
    #button-panel { border: round red; width: 24; align: center middle; padding: 1; }
    Button { height: 3; min-width: 16; content-align: center middle; }
    #enter-btn { background: #7ed957; color: black !important; border: round #7ed957; }
    #instr-btn { background: #ffd966; color: black !important; border: round #ffd966; }
    #clear-btn { background: #e06666; color: white !important; border: round #e06666; }
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
                    with TabPane("Commands", id="cmd-tab"):
                        yield DataTable(id="cmd-table")
                    with TabPane("Instructions", id="help-tab"):
                        yield Static(INSTRUCTIONS, markup=True)
            with Vertical(id="button-panel"):
                yield Button("Enter", id="enter-btn")
                yield Button("Instructions", id="instr-btn")
                yield Button("Clear Log", id="clear-btn")

    def on_mount(self):
        table = self.query_one("#cmd-table", DataTable)
        table.add_columns("Command", "Result")
        table.styles.height = "100%"
        table.cursor_type = "row"
        table.zebra_stripes = True
        self.query_one(Input).focus()
        self.query_one(TabbedContent).active = "cmd-tab"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        input_box = self.query_one(Input)
        tabs = self.query_one("#main-tabs", TabbedContent)
        table = self.query_one("#cmd-table", DataTable)
        
        if btn_id == "enter-btn":
            if input_box.value.strip():
                self.handle_command(input_box.value)
                input_box.value = ""
            input_box.focus()
        elif btn_id == "instr-btn":
            tabs.active = "help-tab"
            table.add_row("Instructions", "Switched to instructions tab")
        elif btn_id == "clear-btn":
            table.clear()
            table.add_columns("Command", "Result")
            tabs.active = "cmd-tab"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value.strip():
            self.handle_command(event.value)
            event.input.value = ""
        event.input.focus()

    def handle_command(self, command):
        command = command.strip()
        if not command:
            return

        table = self.query_one("#cmd-table", DataTable)
        tabs = self.query_one("#main-tabs", TabbedContent)

        if command.lower() == "help":
            tabs.active = "help-tab"
            table.add_row("help", "Switched to instructions tab")
            return

        if command.lower() == "undo":
            result = undo_last()
            table.add_row("undo", result)
            tabs.active = "cmd-tab"
            with open("command_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Command: undo\nResult: {result}\n\n")
            return

        name = extract_name(command)
        intent = predict_intent(command)
        result = to_do_commands(intent, name)
        command_history.append(command)
        
        # Add the command and result to the table
        table.add_row(command, result)
        
        # Ensure we're on the commands tab
        tabs.active = "cmd-tab"
        
        # Log the command
        with open("command_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Command: {command}\nResult: {result}\n\n")

if __name__ == "__main__":
    CommandLogApp().run()