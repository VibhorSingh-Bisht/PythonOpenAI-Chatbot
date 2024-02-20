#note_engine.py
from llama_index.tools import FunctionTool
import os

note_file = os.path.join("data", "notes.txt")

def save_note(note):
    if not os.path.exists(note_file):
        open(note_file, "w")

    with open(note_file, "a") as f:
        f.write(str(note) + "\n")

    return "note saved"

def response_needs_saving(response):

    if (response=="Sorry, I cannot answer your query."):
        return False
    
    return True


note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="This tool can save a text based note to a file for the user",
)
