import os
import subprocess
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def drop(event):
    input_file_path = event.data[1:-1]  # Remove the {} characters
    output_file_path = os.path.splitext(input_file_path)[0] + '.mov'
    subprocess.run(['ffmpeg', '-i', input_file_path, '-c', 'copy', output_file_path], check=True)

root = TkinterDnD.Tk()
root.withdraw()
root.title('Video to MOV converter')

label = tk.Label(root, text='Drag and Drop Video Here', width=40, height=10)
label.pack(expand=1, fill='both')
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', drop)

root.update_idletasks()
root.deiconify()
root.mainloop()
