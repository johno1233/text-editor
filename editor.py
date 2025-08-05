import tkinter as tk
from tkinter import Text, Scrollbar, Menu, messagebox, filedialog
from pygments import lex
from pygments.lexers import PythonLexer

# Create the main window and text area
root = tk.Tk()
root.title("My Wittle Editor")
text = Text(root, wrap='word', undo=True)
scrollbar = Scrollbar(root, command=text.yview)
text.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')
text.pack(side='left', fill='both', expand=true)

# Add syntax Highlighting
text.tag_config("Token.Keyworkd", foreground="blue")
text.tag_config("Token.String", foreground="green")
text.tag_config("Token.Comment", foreground="gray")
text.tag_config("Token.Number", foreground="red")
text.tag_config("Token.Operator", foreground="purple")
text.tag_config("Token.Punctuation", foreground="black")
text.tag_config("Token.Name", foreground="black")
text.tag_config("Token.Literal", foreground="orange")

def highlight():
    content = text.get("1.0", "end-1c")
    text.mark_set("range_start", "1.0")
    for token, content in lex(content, PythonLexer()):
        text.mark_set("range_end", "range_start + %dc" % len(content))
        text.tag_add(str(token), "range_start", "range_end")
        text.mark_set("range_start", "range_end")

highlight_timer = None

def schedule_highlight():
    global highlight_timer
    if highlight_timer is not None:
        root.after_cancel(highlight_timer)
    highlight_timer = root.after(500, highlight)

text.bing("<KeyRelease>", lambda event: schedule_highlight())

# Implement File Operations
menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", comand=save_file)
filemenu.add_command(label="Save As", command=save_as_file)
filemenu.add_seperator()
filemenu.add_command(label="Exit", command=root.quit)

current_file = None

def open_file():
    global currnet_file
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content=file.read()
            text.delete("1.0", tk.END)
            text.insert("1.0", content)
        current_file = file_path
        root.title(f"Text Editor - {file_path}")
        schedule_highlight()
        


