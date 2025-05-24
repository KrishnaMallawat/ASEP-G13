import os
import re
import subprocess
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Static, Input, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical

sentences = [
    "make a folder xyz", "create new folder project", "add a file notes.txt",
    "create file test.py", "delete folder old_project", "remove file trash.py",
    "erase folder backup", "need a new folder", "need a new file",
    "make a folder named xyz", "delete all text files",
    "delete file named creative stuff", "create folder named delete these",
    "delete folder named create jobs", "create file named stuff",
    "remove directory temp", "delete the file called report.docx",
    "make directory logs", "generate a file output.txt", "eliminate folder test_data",
    "copy file data.csv to backup.csv", "move folder images to archive",
    "rename file old.txt to new.txt", "list all files in current directory",
    "show me all folders"
]
labels = [
    "create_folder", "create_folder", "create_file", "create_file",
    "delete_folder", "delete_file", "delete_folder", "create_folder",
    "create_file", "create_folder", "delete_file", "delete_file",
    "create_folder", "delete_folder", "create_file", "delete_folder",
    "delete_file", "create_folder", "create_file", "delete_folder",
    "copy_file", "move_folder", "rename_file", "list_files", "list_folders"
]
model = make_pipeline(CountVectorizer(ngram_range=(1, 3)), LogisticRegression(max_iter=1000))
model.fit(sentences, labels)
history = []

INSTRUCTIONS = (
    "[b yellow]Supported Commands:[/b yellow]\n"
    "- create/make/add/generate a file/folder named <name>\n"
    "- delete/remove/erase/eliminate a file/folder named <name>\n"
    "- list all files\n"
    "- show me all folders\n"
    "- undo (reverts last create/delete)\n"
    "\n[b yellow]Examples:[/b yellow]\n"
    "  create folder test123\n"
    "  delete file old.txt\n"
    "  list files\n"
    "  undo"
)

def extract_name(command):
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
            return f"[green] Folder '{name}' created.[/green]"
        elif intent == "create_file":
            open(name, 'w').close()
            history.append(('delete_file', name))
            return f"[green] File '{name}' created.[/green]"
        elif intent == "delete_folder":
            if os.path.isdir(name):
                os.system(f"rm -rf {name}")
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
        elif intent == "list_files":
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            return "[b]Files:[/b]\n" + ("\n".join(files) if files else "[dim]No files found.[/dim]")
        elif intent == "list_folders":
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
            return "[b]Folders:[/b]\n" + ("\n".join(folders) if folders else "[dim]No folders found.[/dim]")
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
            os.system(f"rm -rf {name}")
            return f"[red] Undo: Folder '{name}' deleted.[/red]"
        elif last_action == 'delete_file':
            os.remove(name)
            return f"[red] Undo: File '{name}' deleted.[/red]"
        elif last_action == 'create_folder':
            os.makedirs(name, exist_ok=True)
            return f"[green] Undo: Folder '{name}' re-created.[/green]"
        elif last_action == 'create_file':
            open(name, 'w').close()
            return f"[green] Undo: File '{name}' re-created.[/green]"
    except Exception as e:
        return f"[red] Undo failed: {str(e)}[/red]"
    return "[yellow]Undo not supported for this action.[/yellow]"

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
                        table = DataTable(zebra_stripes=True)
                        table.add_columns("Command", "Result")
                        yield table
                    with TabPane("Instructions", id="help-tab"):
                        yield Static(INSTRUCTIONS, markup=True)
            with Vertical(id="button-panel"):
                yield Button("Enter", id="enter-btn")
                yield Button("Instructions", id="instr-btn")
                yield Button("Clear Log", id="clear-btn")

    def on_mount(self):
        self.query_one(Input).focus()
        self.query_one(TabbedContent).active = "cmd-tab"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        input_box = self.query_one(Input)
        tabs = self.query_one("#main-tabs", TabbedContent)
        table = self.query_one(DataTable)
        
        if btn_id == "enter-btn":
            self.handle_command(input_box.value)
            input_box.value = ""
            input_box.focus()
        elif btn_id == "instr-btn":
            tabs.active = "help-tab"
        elif btn_id == "clear-btn":
            table.clear(columns=False)
            tabs.active = "cmd-tab"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.handle_command(event.value)
        event.input.value = ""
        event.input.focus()

    def handle_command(self, command):
        command = command.strip()
        tabs = self.query_one("#main-tabs", TabbedContent)
        table = self.query_one(DataTable)

        if not command:
            table.add_row("[yellow]No command entered[/yellow]", "")
            return
        if command.lower() == "help":
            tabs.active = "help-tab"
            return
        if command.lower() == "undo":
            result = undo_last()
            table.add_row("[cyan]undo[/cyan]", result)
            tabs.active = "cmd-tab"
            with open("command_log.txt", "a", encoding="utf-8") as f:
                f.write(f"Command: undo\nResult: {result}\n\n")
            return

        name = extract_name(command)
        intent = model.predict([command])
        result = to_do_commands(intent, name)
        table.add_row(f"[green]{command}[/green]", result)
        tabs.active = "cmd-tab"
        with open("command_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Command: {command}\nResult: {result}\n\n")

if __name__ == "__main__":
    CommandLogApp().run()
