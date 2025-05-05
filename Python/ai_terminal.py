import subprocess
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import difflib

def get_intent(word,command_bits):
    if word in ["make" , "add" ,"new"]:
        command_part=command_bits[command_bits.index(word):]
        for info in command_part:
            if info=="file":
                return "create_file"
            if info=="folder":
                return "create_folder"
    if word in ["delete" , "remove" , "erase"]:
        command_part=command_bits[command_bits.index(word):]
        for info in command_part:
            if info=="file":
                return "delete_file"
            if info=="folder":
                return "delete_folder"
                
def to_do_commands(intent,name):
    
    if intent=="create_folder":
        os.makedirs(name)
    if intent=="create_file":
        open(name,'w').close()
    if intent == "delete_folder":
        try:
            subprocess.run(["rm", "-r", name], check=True)  
            print(f"Folder '{name}' deleted.")
        except subprocess.CalledProcessError:
            print(f"Error: Folder '{name}' could not be deleted.")
    if intent == "delete_file":
        try:
            subprocess.run(["rm", name], check=True)  
            print(f"File '{name}' deleted.")
        except subprocess.CalledProcessError:
            print(f"Error: File '{name}' could not be deleted.")
    

sentences = [
    "make a folder xyz",
    "create new folder project",
    "add a file notes.txt",
    "create file test.py",
    "delete folder old_project",
    "remove file trash.py",
    "erase folder backup",
    "need a new folder",
    "need a new file",
    "make a folder named xyz",
    "delete all text files",
    "delete file named creative stuff",
    "create folder named delete these",
    "delete folder named create jobs",
    "create file named stuff",
]

labels = [
    "create_folder",
    "create_folder",
    "create_file",
    "create_file",
    "delete_folder",
    "delete_file",
    "delete_folder",
    "create_folder",
    "create_file",
    "create_folder", 
    "delete_file",
    "delete_file",
    "create_folder",
    "delete_folder",
    "create_file"
]
model = make_pipeline(CountVectorizer(ngram_range=(1, 3)), LogisticRegression())
model.fit(sentences, labels)

command_list=["cd","ls","mkdir","echo","touch","cat"]

run = True

while(run):
    print("$ ",end='')
    command=input()
    command_bits=command.split(" ")
    
    if(command_bits[0]=="quit"):
        run = False
        
    if command_bits[0] =="do":
        if "name" in command_bits:
            name=command_bits[command_bits.index("name")+1]
        elif "named" in command_bits:
            name=command_bits[command_bits.index("named")+1]
        else:
            name="unnamed"
        
        intent=model.predict([command])
        to_do_commands(intent,name)
        
    elif command_bits[0] in command_list:
        subprocess.run(command_bits[0])
        
