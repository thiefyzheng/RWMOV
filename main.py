import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD
import mimetypes

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
            if os.path.isfile(input_file_path) and not input_file_path.endswith('.mp4'):  # Check if it's a file and not already .mov
                mimetype = mimetypes.guess_type(input_file_path)[0]  # Guess the mimetype of the file
                if mimetype and mimetype.startswith('video'):  # Check if the mimetype starts with 'video'
                    convert_to_mp4(input_file_path)
    elif os.path.isfile(path) and not path.endswith('.mp4'):  # Check if the path is a file and not already .mov
        mimetype = mimetypes.guess_type(path)[0]  # Guess the mimetype of the file
        if mimetype and mimetype.startswith('video'):  # Check if the mimetype starts with 'video'
            convert_to_mp4(path)


import platform


def convert_to_mp4(input_file_path):
    output_file_path = os.path.splitext(input_file_path)[0] + '.mp4'

    # Get the codec information
    codec_info = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of',
         'default=noprint_wrappers=1:nokey=1', input_file_path], capture_output=True, text=True).stdout.strip()

    # Check if the codec is supported by MOV
    if codec_info in ['h264', 'mpeg4', 'aac']:
        # Copy the stream if the codec is supported
        if platform.system() == 'Darwin':  # Check if the operating system is macOS
            subprocess.run(
                ['ffmpeg', '-y', '-i', input_file_path, '-c:v', 'h264_videotoolbox', '-c:a', 'copy', output_file_path],
                check=True)
        elif platform.system() == 'Windows':  # Check if the operating system is Windows
            gpu_info = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], capture_output=True,
                                      text=True).stdout
            if 'NVIDIA' in gpu_info:  # Check if an NVIDIA GPU is available
                subprocess.run(
                    ['ffmpeg', '-y', '-hwaccel', 'cuda', '-i', input_file_path, '-c:v', 'h264_nvenc', '-c:a', 'copy',
                     output_file_path], check=True)
            else:  # Fallback to software encoding
                subprocess.run(
                    ['ffmpeg', '-y', '-i', input_file_path, '-c:v', 'libx264', '-c:a', 'aac', output_file_path],
                    check=True)
        else:  # Fallback to software encoding for other operating systems
            subprocess.run(['ffmpeg', '-y', '-i', input_file_path, '-c:v', 'libx264', '-c:a', 'aac', output_file_path],
                           check=True)
    else:
        # Re-encode the video if the codec is not supported
        subprocess.run(['ffmpeg', '-y', '-i', input_file_path, '-c:v', 'libx264', '-c:a', 'aac', output_file_path],
                       check=True)

    text.set(text.get() + '\nConverted: ' + os.path.basename(
        input_file_path))  # Update the label text with just the filename


def open_file_dialog():
    path = filedialog.askdirectory()  # Open the file dialog to select a directory
    process_path(path)

def open_single_file_dialog():
    path = filedialog.askopenfilename()  # Open the file dialog to select a single file
    process_path(path)

root = TkinterDnD.Tk()
root.withdraw()
root.title('Video to MP4 converter')

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
