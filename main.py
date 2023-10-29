import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD

def drop(event):
    path = event.data
    if platform.system() == 'Windows':  # Check if the operating system is Windows
        path = path[1:-1]  # Remove the {} characters for Windows
        path = path.replace('/', '\\')  # Replace / with \ for Windows paths

    process_path(path)

def process_path(path):
    if os.path.isdir(path):  # Check if the path is a directory
        for filename in os.listdir(path):
            input_file_path = os.path.join(path, filename)
            if os.path.isfile(input_file_path) and not input_file_path.endswith('.mov'):  # Check if it's a file and not already .mov
                convert_to_mov(input_file_path)
    elif os.path.isfile(path) and not path.endswith('.mov'):  # Check if the path is a file and not already .mov
        convert_to_mov(path)

def convert_to_mov(input_file_path):
    output_file_path = os.path.splitext(input_file_path)[0] + '.mov'
    subprocess.run(['ffmpeg', '-y', '-i', input_file_path, '-c', 'copy', output_file_path], check=True)
    text.set(text.get() + '\nConverted: ' + os.path.basename(input_file_path))  # Update the label text with just the filename

def open_file_dialog():
    path = filedialog.askdirectory()  # Open the file dialog to select a directory
    process_path(path)

def open_single_file_dialog():
    path = filedialog.askopenfilename()  # Open the file dialog to select a single file
    process_path(path)

root = TkinterDnD.Tk()
root.withdraw()
root.title('Video to MOV converter')

text = StringVar()

# Only enable drag and drop on non-macOS platforms
if platform.system() != 'Darwin':
    text.set('Drag and Drop Video Here')
else:
    text.set('🍎')

label = tk.Label(root, textvariable=text, width=40, height=10)
label.pack(expand=1, fill='both')

if platform.system() != 'Darwin':
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)

folder_button = tk.Button(root, text='Select Folder', command=open_file_dialog)
folder_button.pack()

file_button = tk.Button(root, text='Select File', command=open_single_file_dialog)
file_button.pack()

root.update_idletasks()
root.deiconify()
root.mainloop()
