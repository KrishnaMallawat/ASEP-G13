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
    "undo last command", "revert previous action",
    # Copy file/folder
    "copy file demo.txt to test.txt", "copy file test.txt to demo.txt",
    "copy folder project to project_backup", "copy folder demo to demo_backup",
    "duplicate file a.txt as b.txt", "duplicate folder foo as bar"
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
    "undo", "undo",
    # Copy file/folder
    "copy_file", "copy_file",
    "copy_folder", "copy_folder",
    "copy_file", "copy_folder"
]

model = make_pipeline(
    CountVectorizer(ngram_range=(1, 3), analyzer='char_wb'),
    LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')
)
model.fit(sentences, labels)
history = []
command_history = []

INSTRUCTIONS = (
    "[b]Supported Commands:[/b]\n"
    "- [#87CEEB]create[/#87CEEB]/[#87CEEB]make[/#87CEEB]/[#87CEEB]add[/#87CEEB]/[#87CEEB]generate[/#87CEEB] a [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] named [#FFA07A]<name>[/#FFA07A]\n"
    "- [#FF9999]delete[/#FF9999]/[#FF9999]remove[/#FF9999]/[#FF9999]erase[/#FF9999]/[#FF9999]eliminate[/#FF9999] a [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] named [#FFA07A]<name>[/#FFA07A]\n"
    "- [#B8860B]rename[/#B8860B]/[#B8860B]change[/#B8860B]/[#B8860B]move[/#B8860B]/[#B8860B]switch[/#B8860B] [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] [#FFA07A]<oldname>[/#FFA07A] to [#FFA07A]<newname>[/#FFA07A]\n"
    "- [#B8860B]rename all[/#B8860B] [#FFA07A]<ext1>[/#FFA07A] files to [#FFA07A]<ext2>[/#FFA07A]\n"
    "- [#4682B4]copy[/#4682B4]/[#4682B4]duplicate[/#4682B4] [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] [#FFA07A]<source>[/#FFA07A] to [#FFA07A]<destination>[/#FFA07A]\n"
    "- [#4682B4]search[/#4682B4]/[#4682B4]find[/#4682B4]/[#4682B4]look for[/#4682B4] [#FFA07A]<text>[/#FFA07A] in [#DDA0DD]<file>[/#DDA0DD]\n"
    "- [#9370DB]show[/#9370DB]/[#9370DB]display[/#9370DB] disk usage\n"
    "- [#9370DB]show[/#9370DB]/[#9370DB]display[/#9370DB] command history\n"
    "- [#9370DB]list[/#9370DB]/[#9370DB]show[/#9370DB]/[#9370DB]display[/#9370DB] all [#DDA0DD]files[/#DDA0DD]/[#98FB98]folders[/#98FB98]\n"
    "- [#CD853F]undo[/#CD853F] (reverts last action)\n"
    "\n[b]Examples:[/b]\n"
    "  [#87CEEB]create[/#87CEEB] [#98FB98]folder[/#98FB98] [#FFA07A]test123[/#FFA07A]\n"
    "  [#87CEEB]create[/#87CEEB] [#DDA0DD]file[/#DDA0DD] [#FFA07A]data.csv[/#FFA07A]\n"
    "  [#FF9999]delete[/#FF9999] [#DDA0DD]file[/#DDA0DD] [#FFA07A]old.txt[/#FFA07A]\n"
    "  [#B8860B]rename[/#B8860B] [#DDA0DD]file[/#DDA0DD] [#FFA07A]old.txt[/#FFA07A] to [#FFA07A]new.txt[/#FFA07A]\n"
    "  [#B8860B]rename all[/#B8860B] [#FFA07A].txt[/#FFA07A] files to [#FFA07A].md[/#FFA07A]\n"
    "  [#4682B4]copy[/#4682B4] [#DDA0DD]file[/#DDA0DD] [#FFA07A]demo.txt[/#FFA07A] to [#FFA07A]test.txt[/#FFA07A]\n"
    "  [#4682B4]copy[/#4682B4] [#98FB98]folder[/#98FB98] [#FFA07A]project[/#FFA07A] to [#FFA07A]project_backup[/#FFA07A]\n"
    "  [#4682B4]search[/#4682B4] [#FFA07A]hello[/#FFA07A] in [#DDA0DD]notes.txt[/#DDA0DD]\n"
    "  [#9370DB]show[/#9370DB] disk usage\n"
    "  [#9370DB]list[/#9370DB] [#DDA0DD]files[/#DDA0DD]\n"
    "  [#CD853F]undo[/#CD853F]\n"
    "\n[dim]Note: All commands are case-insensitive. Command log is saved to command_log.txt[/dim]"
)
def extract_name(command):
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
        elif intent == "copy_file":
            try:
                source, destination = [s.strip() for s in name.split(" to ")] if " to " in name else [s.strip() for s in name.split(" as ")]
                if not os.path.isfile(source):
                    return f"[yellow]Source file '{source}' does not exist.[/yellow]"
                if os.path.exists(destination):
                    return f"[red] Error: Destination '{destination}' already exists.[/red]"
                shutil.copy2(source, destination)
                history.append(('delete_file', destination))
                return f"[green]File copied from '{source}' to '{destination}'.[/green]"
            except Exception as e:
                return f"[red]Error copying file: {str(e)}[/red]"
        elif intent == "copy_folder":
            try:
                source, destination = [s.strip() for s in name.split(" to ")] if " to " in name else [s.strip() for s in name.split(" as ")]
                if not os.path.isdir(source):
                    return f"[yellow]Source folder '{source}' does not exist.[/yellow]"
                if os.path.exists(destination):
                    return f"[red] Error: Destination folder '{destination}' already exists.[/red]"
                shutil.copytree(source, destination)
                history.append(('delete_folder', destination))
                return f"[green]Folder copied from '{source}' to '{destination}'.[/green]"
            except Exception as e:
                return f"[red]Error copying folder: {str(e)}[/red]"
        else:
            return "[magenta] Unknown or unsupported intent.[/magenta]"
    except Exception as e:
        return f"[red] Error: {str(e)}[/red]"

def undo_last():
    if not history:
        return "[yellow]Nothing to undo.[/yellow]"
    last_action, name = history.pop()
    try:
        if last_action == 'delete_folder':
            if os.path.isdir(name):
                shutil.rmtree(name)
                return f"[red] Undo: Folder '{name}' deleted.[/red]"
            else:
                return f"[yellow] Folder '{name}' does not exist for undo.[/yellow]"
        elif last_action == 'delete_file':
            if os.path.isfile(name):
                os.remove(name)
                return f"[red] Undo: File '{name}' deleted.[/red]"
            else:
                return f"[yellow] File '{name}' does not exist for undo.[/yellow]"
        elif last_action == 'create_folder':
            os.makedirs(name, exist_ok=True)
            return f"[green] Undo: Folder '{name}' re-created.[/green]"
        elif last_action == 'create_file':
            open(name, 'w').close()
            return f"[green] Undo: File '{name}' re-created.[/green]"
    except Exception as e:
        return f"[red] Undo failed: {str(e)}[/red]"
    return "[yellow]Undo not supported for this action.[/yellow]"

def predict_intent(command):
    # Special case for search commands
    if any(command.lower().startswith(x) for x in ['search', 'find', 'look for']):
        return 'search_in_file'
    return model.predict([command])[0]

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
    #header { content-align: center middle; height: 3; width: 90%; }
    #command_input { width: 90%; border: round blue; margin-bottom: 1; }
    """

    TITLE = "AI Terminal"

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
        
        if btn_id == "enter-btn":
            if input_box.value.strip():
                self.handle_command(input_box.value)
                input_box.value = ""
            input_box.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value.strip():
            self.handle_command(event.value)
            event.input.value = ""
        event.input.focus()

    def handle_command(self, command):
        command = command.strip()
        if not command:
            return

        if command.lower() == "help":
            self.query_one("#main-tabs", TabbedContent).active = "help-tab"
            return

        if command.lower() == "undo":
            result = undo_last()
            with open("command_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Command: undo\nResult: {result}\n\n")
            return

        name = extract_name(command)
        intent = predict_intent(command)
        result = to_do_commands(intent, name)
        command_history.append(command)
        
        # Log the command
        with open("command_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Command: {command}\nResult: {result}\n\n")

if __name__ == "__main__":
    CommandLogApp().run()