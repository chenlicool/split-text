import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

def is_chinese_char(char):
    """Check if a character is a Chinese character."""
    return '\u4e00' <= char <= '\u9fff'

def split_text_file(input_file, chinese_output, english_output):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        chinese_lines = []
        english_lines = []
        is_english_block = False

        for line in lines:
            # Check if the line is a timestamp or a sequence number
            if line.strip().isdigit() or '-->' in line:
                chinese_lines.append(line)
                english_lines.append(line)
            elif is_chinese_char_in_line(line):
                chinese_lines.append(line)
            elif not is_chinese_char_in_line(line):
                english_lines.append(line)
            else:
                chinese_lines.append(line)
                english_lines.append(line)

        with open(chinese_output, 'w', encoding='utf-8') as chinese_file:
            chinese_file.writelines(chinese_lines)

        with open(english_output, 'w', encoding='utf-8') as english_file:
            english_file.writelines(english_lines)
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to split files: {e}")
        return False

def is_chinese_char_in_line(line):
    """Check if any character in the line is a Chinese character."""
    return any(is_chinese_char(char) for char in line)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

def start_split():
    input_file = input_file_entry.get()
    if not input_file:
        messagebox.showwarning("Warning", "Please select a file.")
        return
    
    base_dir = os.path.dirname(input_file)
    chinese_output = os.path.join(base_dir, 'output_chinese.txt')
    english_output = os.path.join(base_dir, 'output_english.txt')

    success = split_text_file(input_file, chinese_output, english_output)
    if success:
        messagebox.showinfo("Success", "Files split successfully!")
        subprocess.run(["open", base_dir])  # Open the directory in macOS

# 创建主窗口
root = tk.Tk()
root.title("Text File Splitter")

# 创建并放置标签和按钮
tk.Label(root, text="Select a text file to split:").grid(row=0, column=0, padx=10, pady=10)
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)
tk.Button(root, text="Start", command=start_split).grid(row=1, column=0, columnspan=3, pady=10)

# 运行主循环
root.mainloop()
