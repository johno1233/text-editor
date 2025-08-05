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
        
def save_file():
    global currnet_file
    if current_file:
        with open(current_file, "w") as file:
            content = text.get("1.0", "end-1c")
            file.write(content)
    else:
        save_as_file()

def save_as_file():
    global current_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            content = text.get("1.0", "end-1c")
            file.write(content)
        current_file = file_path
        root.title(f"Text Editor - {file_path}")

# Add Vim Motions
current_mode = "normal"

def enter_insert_mode(event=None):
    global current_mode
    current_mode = "insert"
    text.config(insertwidth=2)
    text.unbind("<Key>")

def enter_normal_mode(event=None):
    global current_mode
    current_mode = "normal"
    text.config(insertwidth=1)
    text.bind("<Key>", normal_mode_key)

text.bind("<Escape>", enter_normal_mode)

def move_left():
    current_pos = text.index(tk.INSERT)
    line, col = map(int, current_pos.split("."))
    if col > 0
        new_pos = f"{line}.{col-1}"
        text.mark_set(tk.INSERT, new_pos)
        text.see(tk.INSERT)

def move_right():
    current_pos = text.index(tk.INSERT)
    line, col = map(int, current_pos,split("."))
    line_count = int(text.index("end-1c").split(".")[0])
    if col < len(text.get(f"{line}.0", f"{line}.end")) - 1:
        new_pos = f"{line}.{col+1}"
        text.mark_set(tk.INSERT, new_pos)
        text.see(tk.INSERT)
    elif line < line_count:
        new_pos = f"{line+1}.0"
        text.mark_set(tk.INSERT, new_pos)
        text.see(tk.INSERT)

def move_up()
    current_pos = text.index(tk.INSERT)
    line, col = map(int, current_pos.split("."))
    if line > 1:
        prev_line = line - 1
        prev_line_text = text.get(f"{prev_line}.0", f"{prev_line}.end")
        if col < len(prev_line_text) - 1:
            new_pos = f"{prev_line}.{col}"
        else:
            new_pos = f"{prev_line}.end-1c"
        text.mark_set(tk.INSERT, new_pos)
        text.see(tk.INSERT)
