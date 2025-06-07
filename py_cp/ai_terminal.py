import os
import re
import shutil
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Static, Input, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical
import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import random

# Expanded training data for better natural language support
# Search operations
sentences = [
    "search hello in file.txt", "find error in log.txt", "look for world in notes.md",
    "search for text in file.txt", "find the word hello in test.txt",
    "search 'hello world' in file.txt", "find \"error message\" in log.txt",
    "look up debug in app.log", "search for password in config.txt",
    "find the phrase hello world in doc.txt",

    # Rename operations (file and folder)
    "rename file old.txt to new.txt", "rename folder oldfolder to newfolder",
    "rename old.txt to new.txt", "rename oldfolder to newfolder",
    "change file a.txt to b.txt", "change folder a to b",
    "move file a.txt to b.txt", "move folder a to b",
    "rename notes.md as notes_final.md", "switch script.py to script_v2.py",
    "rename backups as backups_archive", "switch music to music_collection",
    "rename all .txt files to .md", "rename all .log files to .bak",

    # Create file/folder operations
    "make a folder xyz", "create new folder project", "add a file notes.txt",
    "create file test.py", "new file report.txt", "create a new file called data.csv",
    "make file notes.md", "generate file summary.docx", "add file script.py",
    "new folder images", "create a new folder called docs", "make directory backups",
    "add folder music", "generate folder videos",
    "create folder name happy and jump","make these files new.txt and old.txt",
    "new folders willy and wonka neede", "need the files afhsan.py and kaushal.py here",
    "can u make a folder called images, static, templates", "can u make files called acer.py ros.cpp and node.sh"

    # Repetitive variants (testing robustness)
    "make fil.txt", "create fil.txt", "add fil.txt", "generate fil.txt", "new fil.txt",
    "make file fil.txt", "create file fil.txt", "add file fil.txt", "generate file fil.txt", "new file fil.txt",

    # Delete operations
    "delete folder old_project", "remove file trash.py", "erase folder backup",
    "delete file named creative stuff", "eliminate folder named delete these",
    "delete folder named create jobs", "delete file named stuff",
    "remove directory temp", "delete the file called report.docx",
    "erase directory logs", "generate a file output.txt", "eliminate folder test_data",
    "remove report.txt", "delete the file data.csv", "erase file notes.md",
    "eliminate script.py", "trash file summary.docx",
    "remove images", "delete the folder docs", "erase folder backups",
    "eliminate directory music", "trash folder videos","erase happy and jump folder",
    "remove flash.py home.html and home.css","remove all these aayush and harshvardhan",
    "eliminate folder final_older and final_oldest","wipe these files latest_edit.py term_project.py",
    "discard new folders i made"," discard all files in the directory python"

    # Listing files and folders
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
    # Search
    "search_in_file", "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file", "search_in_file",
    "search_in_file",

    # Rename (file/folder)
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_folder",
    "rename_file", "rename_file",
    "rename_folder", "rename_folder",
    "rename_multiple_files", "rename_multiple_files",

    # Create file/folder
    "create", "create", "create",
    "create", "create", "create",
    "create", "create", "create",
    "create", "create", "create",
    "create", "create","create", "create",
    "create", "create","create", "create",

    # Repetitive (fil.txt variants)
    "create", "create", "create", "create", "create",
    "create", "create", "create", "create", "create",

    # Delete operations
    "delete", "delete", "delete",
    "delete", "delete","delete",
    "delete", "delete","delete",
    "delete", "delete","delete",
    "delete", "delete", "delete",
    "delete", "delete", "delete",
    "delete", "delete",
    "delete", "delete", "delete",
    "delete", "delete",
    "delete", "delete",
    

    # List
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


intent_model = make_pipeline(
    CountVectorizer(ngram_range=(1, 3), analyzer='char_wb'),
    LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced')
)
intent_model.fit(sentences, labels)
history = []
command_history = []

def get_fixed_training_data():
    data = [
        ("Create folders named happy and jump.", [["happy", "folder"], ["jump", "folder"]]),
        ("Delete folders called alpha and beta.", [["alpha", "folder"], ["beta", "folder"]]),
        ("Make a folder named gamma.", [["gamma", "folder"]]),
        ("Remove the folders blue and red.", [["blue", "folder"], ["red", "folder"]]),
        ("Erase folder called zoom and zip.", [["zoom", "folder"], ["zip", "folder"]]),
        ("Make folders wuss and wompy.", [["wuss", "folder"], ["wompy", "folder"]]),
        ("Create directories named swing and pop.", [["swing", "folder"], ["pop", "folder"]]),
        ("Remove folders kite and kite2.", [["kite", "folder"], ["kite2", "folder"]]),
        ("make a folder xyz", [["xyz", "folder"]]),
        ("create new folder project", [["project", "folder"]]),
        ("add a file notes.txt", [["notes.txt", "file"]]),
        ("create file test.py", [["test.py", "file"]]),
        ("delete folder old_project", [["old_project", "folder"]]),
        ("remove file trash.py", [["trash.py", "file"]]),
        ("erase folder backup", [["backup", "folder"]]),
        ("need these folders- images, static  and templates", [["images", "folder"], ["static", "folder"], ["templates", "folder"]]),
        ("need a new file stuff.py, stuff.cpp in the folder node", [["stuff.py", "file"], ["stuff.cpp", "file"], ["node", "folder"]]),
        ("make a folder named xyz", [["xyz", "folder"]]),
        ("delete all text files", [["text", "file"]]),
        ("delete file named creative_stuff", [["creative_stuff", "file"]]),
        ("create folder named delete_these", [["delete_these", "folder"]]),
        ("delete folder named create jobs", [["create_jobs", "folder"]]),
        ("create a file report_final.docx", [["report_final.docx", "file"]]),
        ("add folders: scripts, modules, assets", [["scripts", "folder"], ["modules", "folder"], ["assets", "folder"]]),
        ("make new folder called logs_2024", [["logs_2024", "folder"]]),
        ("remove old folders temp1, temp2", [["temp1", "folder"], ["temp2", "folder"]]),
        ("create directory test_data", [["test_data", "folder"]]),
        ("delete backup.zip", [["backup.zip", "file"]]),
        ("add folder configs", [["configs", "folder"]]),
        ("create a folder build-output", [["build-output", "folder"]]),
        ("remove all folders with name tmp1 and tmp_2", [["tmp1", "folder"], ["tmp_2", "folder"]]),
        ("delete logs, reports and exports folders", [["logs", "folder"], ["reports", "folder"], ["exports", "folder"]]),
        ("create a file todo_list.md", [["todo_list.md", "file"]]),
        ("make a folder named api_endpoints", [["api_endpoints", "folder"]]),
        ("create a folder structure src, include, bin", [["src", "folder"], ["include", "folder"], ["bin", "folder"]]),
        ("erase the folder old_code", [["old_code", "folder"]]),
        ("delete notes_old.txt file", [["notes_old.txt", "file"]]),
        ("create folders user_data, system32", [["user_data", "folder"], ["system32", "folder"]]),
        ("remove image files img001.jpg img002.jpg", [["img001.jpg", "file"], ["img002.jpg", "file"]]),
        ("add test case file test_case01.cpp", [["test_case01.cpp", "file"]]),
        ("create folder release_2023", [["release_2023", "folder"]]),
        ("delete build and dist folders", [["build", "folder"], ["dist", "folder"]]),
        ("create main.cpp and main.py", [["main.cpp", "file"], ["main.py", "file"]]),
        ("remove index.html and style.css", [["index.html", "file"], ["style.css", "file"]]),
        ("add file named input_data.json", [["input_data.json", "file"]]),
        ("create folders src/components and src/utils", [["src/components", "folder"], ["src/utils", "folder"]]),
        ("delete the folder output/logs", [["output/logs", "folder"]]),
        ("make new directory data-processing", [["data-processing", "folder"]]),
        ("create hidden folder .config", [[".config", "folder"]]),
        ("delete the file .env", [[".env", "file"]]),
        ("add folder named archive_2022", [["archive_2022", "folder"]]),
        ("erase file called scratch.py", [["scratch.py", "file"]]),
        ("create report.csv and summary.csv files", [["report.csv", "file"], ["summary.csv", "file"]]),
        ("make folders test_env and prod_env", [["test_env", "folder"], ["prod_env", "folder"]]),
        ("create folders temp-data and misc", [["temp-data", "folder"], ["misc", "folder"]]),
        ("delete old_data_backup folder", [["old_data_backup", "folder"]]),
        ("create a directory analysis_results", [["analysis_results", "folder"]]),
        ("remove pdfs sample1.pdf and sample2.pdf", [["sample1.pdf", "file"], ["sample2.pdf", "file"]]),
        ("make folder logs/temp", [["logs/temp", "folder"]]),
        ("create script.sh and deploy.sh files", [["script.sh", "file"], ["deploy.sh", "file"]]),
        ("remove debug.log file", [["debug.log", "file"]]),
        ("add config.ini file", [["config.ini", "file"]]),
        ("create folders snapshots and preview", [["snapshots", "folder"], ["preview", "folder"]]),
        ("delete the folder test_run_03", [["test_run_03", "folder"]]),
        ("make files main_test.cpp, helper_test.cpp", [["main_test.cpp", "file"], ["helper_test.cpp", "file"]]),
        ("create folder _cache_", [["_cache_", "folder"]]),
        ("remove folders archive_2020 and archive_2021", [["archive_2020", "folder"], ["archive_2021", "folder"]]),
        ("add documents doc1.docx and doc2.docx", [["doc1.docx", "file"], ["doc2.docx", "file"]]),
        ("create hidden file .gitignore", [[".gitignore", "file"]]),
        ("delete file readme.txt", [["readme.txt", "file"]]),
        ("make folders dummy1, dummy2, and dummy3", [["dummy1", "folder"], ["dummy2", "folder"], ["dummy3", "folder"]]),
        ("add source.cpp and test.cpp", [["source.cpp", "file"], ["test.cpp", "file"]]),
        ("remove cache and bin folders", [["cache", "folder"], ["bin", "folder"]]),
        ("create directory scripts/utils", [["scripts/utils", "folder"]]),
        ("make files task1.py task2.py", [["task1.py", "file"], ["task2.py", "file"]]),
        ("delete all .log files", [["log", "file"]]),
        ("add test_input.txt and output_data.txt", [["test_input.txt", "file"], ["output_data.txt", "file"]]),
        ("remove folder __pycache__", [["__pycache__", "folder"]]),
        ("create folders alpha_beta and gamma-delta", [["alpha_beta", "folder"], ["gamma-delta", "folder"]]),
        ("delete temporary.json and data.xml", [["temporary.json", "file"], ["data.xml", "file"]]),
        ("make folders a1, b2, c3", [["a1", "folder"], ["b2", "folder"], ["c3", "folder"]]),
        ("create files x.py, y.py, z.py", [["x.py", "file"], ["y.py", "file"], ["z.py", "file"]]),
        ("remove script_old.sh", [["script_old.sh", "file"]]),
        ("delete folders with names node_1 and node-2", [["node_1", "folder"], ["node-2", "folder"]]),
        ("add folders features and logs_debug", [["features", "folder"], ["logs_debug", "folder"]]),
        ("create the directory output_merged", [["output_merged", "folder"]]),
        ("delete the old_research folder", [["old_research", "folder"]]),
        ("remove file final_results.csv", [["final_results.csv", "file"]]),
        ("create test files case1.txt case2.txt case3.txt", [["case1.txt", "file"], ["case2.txt", "file"], ["case3.txt", "file"]]),
        ("make new folders helper_functions and test_suite", [["helper_functions", "folder"], ["test_suite", "folder"]]),
        ("add folder configs/debug", [["configs/debug", "folder"]]),
        ("delete files draft1.docx and draft2.docx", [["draft1.docx", "file"], ["draft2.docx", "file"]]),
        ("create examples folder", [["examples", "folder"]]),
        ("erase notes folder", [["notes", "folder"]]),
        ("remove archive.zip file", [["archive.zip", "file"]]),
        ("delete crash.log and debug.log", [["crash.log", "file"], ["debug.log", "file"]]),
        ("make folder markdown_docs", [["markdown_docs", "folder"]]),
        ("create directory _old_logs_", [["_old_logs_", "folder"]]),
        
        # 50 entries with both files and folders
        ("Create a folder named logs and add file server.log", [["logs", "folder"], ["server.log", "file"]]),
        ("Make folders bin and include and files main.cpp and utils.cpp", [["bin", "folder"], ["include", "folder"], ["main.cpp", "file"], ["utils.cpp", "file"]]),
        ("Add folders test_cases and docs with files test1.py and readme.md", [["test_cases", "folder"], ["docs", "folder"], ["test1.py", "file"], ["readme.md", "file"]]),
        ("Create directory assets and place file logo.png inside", [["assets", "folder"], ["logo.png", "file"]]),
        ("Generate folders images, thumbnails and files pic1.jpg, pic2.jpg", [["images", "folder"], ["thumbnails", "folder"], ["pic1.jpg", "file"], ["pic2.jpg", "file"]]),
        ("Make folders data/input and data/output and add files input.txt and result.csv", [["data/input", "folder"], ["data/output", "folder"], ["input.txt", "file"], ["result.csv", "file"]]),
        ("Set up folder scripts and create files run.sh and build.sh", [["scripts", "folder"], ["run.sh", "file"], ["build.sh", "file"]]),
        ("Create folders logs_2022 and logs_2023 and files log1.txt and log2.txt", [["logs_2022", "folder"], ["logs_2023", "folder"], ["log1.txt", "file"], ["log2.txt", "file"]]),
        ("Add folder images and files index.html and style.css", [["images", "folder"], ["index.html", "file"], ["style.css", "file"]]),
        ("Create folders database and models and file schema.sql", [["database", "folder"], ["models", "folder"], ["schema.sql", "file"]]),
        ("Create folder outputs and files summary.txt, results.txt", [["outputs", "folder"], ["summary.txt", "file"], ["results.txt", "file"]]),
        ("Add folders configs/env and configs/prod and files env.json and prod.json", [["configs/env", "folder"], ["configs/prod", "folder"], ["env.json", "file"], ["prod.json", "file"]]),
        ("Generate folder cache and place files tmp1.txt and tmp2.txt", [["cache", "folder"], ["tmp1.txt", "file"], ["tmp2.txt", "file"]]),
        ("Create folders analytics and insights with reports.csv and trends.csv files", [["analytics", "folder"], ["insights", "folder"], ["reports.csv", "file"], ["trends.csv", "file"]]),
        ("Add project folder and files app.py, requirements.txt", [["project", "folder"], ["app.py", "file"], ["requirements.txt", "file"]]),
        ("Make folder logs/debug and add debug1.log, debug2.log", [["logs/debug", "folder"], ["debug1.log", "file"], ["debug2.log", "file"]]),
        ("Create folders web/assets and web/scripts and add index.html, main.js", [["web/assets", "folder"], ["web/scripts", "folder"], ["index.html", "file"], ["main.js", "file"]]),
        ("Add archive folder and backup.sql file", [["archive", "folder"], ["backup.sql", "file"]]),
        ("Create folders bin/output and bin/logs and files out1.txt and out2.txt", [["bin/output", "folder"], ["bin/logs", "folder"], ["out1.txt", "file"], ["out2.txt", "file"]]),
        ("Generate folder test_data and add data1.csv, data2.csv", [["test_data", "folder"], ["data1.csv", "file"], ["data2.csv", "file"]]),
        ("Add folders videos/raw and videos/edited and files clip1.mp4 and clip2.mp4", [["videos/raw", "folder"], ["videos/edited", "folder"], ["clip1.mp4", "file"], ["clip2.mp4", "file"]]),
        ("Create documentation folder with files intro.md and usage.md", [["documentation", "folder"], ["intro.md", "file"], ["usage.md", "file"]]),
        ("Add src folder and files main.cpp, utils.hpp", [["src", "folder"], ["main.cpp", "file"], ["utils.hpp", "file"]]),
        ("Create project_logs and add log_today.txt and log_yesterday.txt", [["project_logs", "folder"], ["log_today.txt", "file"], ["log_yesterday.txt", "file"]]),
        ("Make folders alpha/test and beta/train with files a.py and b.py", [["alpha/test", "folder"], ["beta/train", "folder"], ["a.py", "file"], ["b.py", "file"]]),
        ("Add directory builds and files version.txt and changelog.txt", [["builds", "folder"], ["version.txt", "file"], ["changelog.txt", "file"]]),
        ("Create a folder named final_results and add output1.csv and output2.csv", [["final_results", "folder"], ["output1.csv", "file"], ["output2.csv", "file"]]),
        ("Make folders image_sets and metadata with image1.jpg and meta1.json", [["image_sets", "folder"], ["metadata", "folder"], ["image1.jpg", "file"], ["meta1.json", "file"]]),
        ("Add folders code/java and code/python and add app.java, app.py", [["code/java", "folder"], ["code/python", "folder"], ["app.java", "file"], ["app.py", "file"]]),
        ("Create folder batch_run and files batch1.sh and batch2.sh", [["batch_run", "folder"], ["batch1.sh", "file"], ["batch2.sh", "file"]]),
        ("Create deployment folder with docker-compose.yml and .env file", [["deployment", "folder"], ["docker-compose.yml", "file"], [".env", "file"]]),
        ("Add logs/session and files session1.log session2.log", [["logs/session", "folder"], ["session1.log", "file"], ["session2.log", "file"]]),
        ("Create folders data/json and data/xml with files data1.json and data1.xml", [["data/json", "folder"], ["data/xml", "folder"], ["data1.json", "file"], ["data1.xml", "file"]]),
        ("Make folders fonts and themes with files style.css and theme.json", [["fonts", "folder"], ["themes", "folder"], ["style.css", "file"], ["theme.json", "file"]]),
        ("Add folders tasks/monday and tasks/tuesday with tasks.csv and notes.md", [["tasks/monday", "folder"], ["tasks/tuesday", "folder"], ["tasks.csv", "file"], ["notes.md", "file"]]),
        ("Generate folder simulation with run1.py and results1.txt", [["simulation", "folder"], ["run1.py", "file"], ["results1.txt", "file"]]),
        ("Create temp folder with dump.log and tempdata.json", [["temp", "folder"], ["dump.log", "file"], ["tempdata.json", "file"]]),
        ("Make training folder and add model.pkl and config.yaml", [["training", "folder"], ["model.pkl", "file"], ["config.yaml", "file"]]),
        ("Add folders ref/images and ref/data with img01.png and data.csv", [["ref/images", "folder"], ["ref/data", "folder"], ["img01.png", "file"], ["data.csv", "file"]]),
        ("Create project folders design and prototype with sketch.fig and draft.pdf", [["design", "folder"], ["prototype", "folder"], ["sketch.fig", "file"], ["draft.pdf", "file"]]),
        ("Create folder test_cases and files input1.txt and output1.txt", [["test_cases", "folder"], ["input1.txt", "file"], ["output1.txt", "file"]]),
        ("Generate folders debug_logs and temp_configs and add debug.json, temp.ini", [["debug_logs", "folder"], ["temp_configs", "folder"], ["debug.json", "file"], ["temp.ini", "file"]]),
        ("Add server folder and server.py, server_config.ini files", [["server", "folder"], ["server.py", "file"], ["server_config.ini", "file"]]),
        ("Create folders media/audio and media/video with track.mp3 and clip.mov", [["media/audio", "folder"], ["media/video", "folder"], ["track.mp3", "file"], ["clip.mov", "file"]]),
        ("Create app folder and add app.js and config.js", [["app", "folder"], ["app.js", "file"], ["config.js", "file"]]),
        ("Add folders user/logs and user/data and files info.txt and backup.txt", [["user/logs", "folder"], ["user/data", "folder"], ["info.txt", "file"], ["backup.txt", "file"]]),
        ("Create report folder with report_q1.pdf and report_q2.pdf", [["report", "folder"], ["report_q1.pdf", "file"], ["report_q2.pdf", "file"]]),
        ("Create modules folder and add init.py and parser.py", [["modules", "folder"], ["init.py", "file"], ["parser.py", "file"]]),
        ("Generate folders frontend and backend and files index.js and app.go", [["frontend", "folder"], ["backend", "folder"], ["index.js", "file"], ["app.go", "file"]]),
        ("Add folder storage and files file_a and file_b", [["storage", "folder"], ["file_a", "file"], ["file_b", "file"]]),
        ("Create logs/errors and logs/info with error.log and info.log", [["logs/errors", "folder"], ["logs/info", "folder"], ["error.log", "file"], ["info.log", "file"]]),
        ("Create folder bin/debug and files a.out and debug.txt", [["bin/debug", "folder"], ["a.out", "file"], ["debug.txt", "file"]]),
        ("Add folders generated/css and generated/js and files styles.css and script.js", [["generated/css", "folder"], ["generated/js", "folder"], ["styles.css", "file"], ["script.js", "file"]]),
        ("Create tmp folder and add delete.me and temp.txt", [["tmp", "folder"], ["delete.me", "file"], ["temp.txt", "file"]]),
        ("Make folder logs/runtime with files log_rt1 and log_rt2", [["logs/runtime", "folder"], ["log_rt1", "file"], ["log_rt2", "file"]]),
        ("Create directory notebooks and add analysis.ipynb and explore.ipynb", [["notebooks", "folder"], ["analysis.ipynb", "file"], ["explore.ipynb", "file"]]),
        ("Add backup folder with db_backup.sql and config.bak", [["backup", "folder"], ["db_backup.sql", "file"], ["config.bak", "file"]]),
        ("Create logs/critical and add critical1.txt and critical2.txt", [["logs/critical", "folder"], ["critical1.txt", "file"], ["critical2.txt", "file"]]),
        ("Add data folder and files raw.json and processed.json", [["data", "folder"], ["raw.json", "file"], ["processed.json", "file"]]),
        ("Make archive/2024 and archive/2023 folders with zip1.zip and zip2.zip", [["archive/2024", "folder"], ["archive/2023", "folder"], ["zip1.zip", "file"], ["zip2.zip", "file"]])
    ]   


    TRAIN_DATA = []

    for sentence, things in data:
        entities = []
        for thing, label in things:
            start = sentence.find(thing)
            if start != -1:
                end = start + len(thing)
                entities.append((start, end, label.upper()))
        TRAIN_DATA.append((sentence, {"entities": entities}))

    return TRAIN_DATA

TRAIN_DATA = get_fixed_training_data()

nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

ner.add_label("FILE")
ner.add_label("FOLDER")

optimizer = nlp.begin_training()
for itn in range(45):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=2)
    for batch in batches:
        examples = []
        for text, annots in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annots)
            examples.append(example)
        nlp.update(examples, sgd=optimizer, losses=losses)
    print(f"Iteration {itn+1}, Losses: {losses}")


INSTRUCTIONS = (
    "[b]Supported Commands:[/b]\n"
    "- [#87CEEB]create[/#87CEEB]/[#87CEEB]make[/#87CEEB]/[#87CEEB]add[/#87CEEB]/[#87CEEB]generate[/#87CEEB] a [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] named [#FFA07A]<name>[/#FFA07A]\n"
    "- [#FF9999]delete[/#FF9999]/[#FF9999]remove[/#FF9999]/[#FF9999]erase[/#FF9999]/[#FF9999]eliminate[/#FF9999] a [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] named [#FFA07A]<name>[/#FFA07A]\n"
    "- [#B8860B]rename[/#B8860B]/[#B8860B]change[/#B8860B]/[#B8860B]move[/#B8860B]/[#B8860B]switch[/#B8860B] [#DDA0DD]file[/#DDA0DD]/[#98FB98]folder[/#98FB98] [#FFA07A]<oldname>[/#FFA07A] to [#FFA07A]<newname>[/#FFA07A]\n"
    "- [#B8860B]rename all[/#B8860B] [#FFA07A]<ext1>[/#FFA07A] files to [#FFA07A]<ext2>[/#FFA07A]\n"
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
    "  [#4682B4]search[/#4682B4] [#FFA07A]hello[/#FFA07A] in [#DDA0DD]notes.txt[/#DDA0DD]\n"
    "  [#9370DB]show[/#9370DB] disk usage\n"
    "  [#9370DB]list[/#9370DB] [#DDA0DD]files[/#DDA0DD]\n"
    "  [#CD853F]undo[/#CD853F]\n"
    "\n[dim]Note: All commands are case-insensitive. Command log is saved to command_log.txt[/dim]"
)

def extract_name(command):
    name_model = nlp(command)
    file_name=[ent.text for ent in name_model.ents if ent.label_ == "FILE"]
    folder_name=[ent.text for ent in name_model.ents if ent.label_ == "FOLDER"]

    names={
        "file" : [name for name in file_name],
        "folder" : [name for name in folder_name]
    }

    return names

def to_do_commands(intent, names, self):
    file_names=[name for name in names["file"]]
    folder_names=[name for name in names["folder"]]

    try:
        if intent == "create":
            for name in folder_names:
                os.makedirs(name, exist_ok=True)
                history.append(('create', name))
            for name in file_names:
                open(name, 'w').close()
                history.append(('create', name))
        elif intent == "delete":
            for name in folder_names:
                if os.path.isdir(name):
                    shutil.rmtree(name)
                    history.append(('delete', name))
                else:
                  return f"[yellow]Folder '{name}' does not exist.[/yellow]"
            for name in file_names:
                if os.path.isfile(name):
                    os.remove(name)
                    history.append(('delete', name))
                else:
                    return f"[yellow]File '{name}' does not exist.[/yellow]"
        elif intent == "rename_file" or intent == "rename_folder":
            name = [names for names in folder_names] + [names for names in file_names]
            if " to " in name:
                old_name, new_name = [n.strip() for n in name.split(" to ")]
                if not os.path.exists(old_name):
                    return f"[yellow]'{old_name}' does not exist.[/yellow]"
                os.rename(old_name, new_name)
                return f"[cyan]Renamed '{old_name}' to '{new_name}'.[/cyan]"
            else:
                return "[yellow]Please use the format: rename file old.txt to new.txt[/yellow]"
        elif intent == "rename_multiple_files":
            name = [names for names in folder_names] + [names for names in file_names]
            ext_from, ext_to = [s.strip() for s in name.split(" to ")]
            count = 0
            for fname in os.listdir('.'):
                if fname.endswith(ext_from):
                    new_name = fname[:-len(ext_from)] + ext_to
                    os.rename(fname, new_name)
                    count += 1
            return f"[cyan]Renamed {count} files from {ext_from} to {ext_to}.[/cyan]" if count else f"[yellow]No files with {ext_from} found.[/yellow]"
        elif intent == "search_in_file":
            name = [names for names in file_names]
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
        elif intent == "disk_usage":
            total, used, free = shutil.disk_usage(os.getcwd())
            return (f"[b]Disk Usage:[/b]\n"
                    f"Total: {total // (2**20)} MB\n"
                    f"Used: {used // (2**20)} MB\n"
                    f"Free: {free // (2**20)} MB")
        elif intent == "history":
            if not command_history:
                return "[yellow]No commands in history.[/yellow]"
            return "[b]Command History:[/b]\n" + "\n".join(command_history)
        elif intent == "list_files":
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            if files:
                for file in files:
                    table = self.query_one("#command-table", DataTable)
                    table.add_row(file, "")
                return f"[b]Listed {len(files)} files.[/b]"
            else:
                 return "[dim]No files found.[/dim]"
        elif intent == "list_folders":
            folders = [f for f in os.listdir('.') if os.path.isdir(f)]
            if folders:
                for folder in folders:
                    table = self.query_one("#command-table", DataTable)
                    table.add_row(folder, "")
                return f"[b]Listed {len(folders)} folder(s).[/b]"
            else:
                 return "[dim]No folders found.[/dim]"
        elif intent == "undo":
            return undo_last()
        else:
            return "[magenta]Unknown or unsupported intent.[/magenta]"
    except Exception as e:
        return f"[red]Error: {str(e)}[/red]"


def undo_last():
    if not history:
        return "[yellow]Nothing to undo.[/yellow]"
    last_action, name = history.pop()
    try:
        if last_action == 'delete':
            if os.path.isdir(name):
                shutil.rmtree(name)
                return f"[red]Undo: Folder '{name}' deleted.[/red]"
            else:
                return f"[yellow]Folder '{name}' does not exist for undo.[/yellow]"
        elif last_action == 'delete':
            if os.path.isfile(name):
                os.remove(name)
                return f"[red]Undo: File '{name}' deleted.[/red]"
            else:
                return f"[yellow]File '{name}' does not exist for undo.[/yellow]"
        elif last_action == 'create':
            os.makedirs(name, exist_ok=True)
            return f"[green]Undo: Folder '{name}' re-created.[/green]"
        elif last_action == 'create':
            open(name, 'w').close()
            return f"[green]Undo: File '{name}' re-created.[/green]"
    except Exception as e:
        return f"[red]Undo failed: {str(e)}[/red]"
    return "[yellow]Undo not supported for this action.[/yellow]"

def predict_intent(command):
    if any(command.lower().startswith(x) for x in ['search', 'find', 'look for']):
        return 'search_in_file'
    return intent_model.predict([command])[0]

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

    TITLE = "NLP BASED COMMAND LOGGING"

    def compose(self) -> ComposeResult:
        yield Static(self.TITLE, id="header")
        yield Input(placeholder="Enter command here...", id="command_input")
        with Horizontal(id="main"):
            with Vertical(id="table-panel"):
                with TabbedContent(id="main-tabs"):
                    with TabPane("Commands", id="cmd-tab"):
                        table = DataTable(id="command-table", zebra_stripes=True)
                        table.add_columns("Command", "Result")
                        yield table
                    with TabPane("Instructions", id="help-tab"):
                        yield Static(INSTRUCTIONS, markup=True)
            with Vertical(id="button-panel"):
                yield Button("Enter", id="enter-btn")

    def on_mount(self):
        self.query_one(Input).focus()
        self.query_one(TabbedContent).active = "cmd-tab"

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
        table = self.query_one("#command-table", DataTable)
        if command.lower() == "help":
            self.query_one("#main-tabs", TabbedContent).active = "help-tab"
            return
        names = extract_name(command)
        intent = predict_intent(command)
        result = to_do_commands(intent, names, self)
        command_history.append(command)
        table.add_row( command,result)
        self.query_one("#main-tabs", TabbedContent).active = "cmd-tab"

if __name__ == "__main__":
    CommandLogApp().run()

