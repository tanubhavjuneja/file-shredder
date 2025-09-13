import os
import argparse
import random
import shutil
import sys
import uuid
from tqdm import tqdm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import customtkinter as ctk
from tkinter import filedialog, messagebox
def encrypt_file(file_path):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    with open(file_path, "rb") as f:
        data = f.read()
    if len(data) % 16 != 0:
        data += b" " * (16 - len(data) % 16)
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    with open(file_path, "wb") as f:
        f.write(encrypted_data)
    print(f"File {file_path} encrypted before shredding.")
def overwrite_file(file_path, passes=7):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    encrypt_file(file_path)
    file_size = os.path.getsize(file_path)
    with open(file_path, "wb") as file:
        for _ in tqdm(range(passes), desc=f"Overwriting {file_path}", unit="pass"):
            file.seek(0)
            file.write(os.urandom(file_size))
            file.flush()
            os.fsync(file.fileno())
    for _ in range(passes):
        random_name = str(uuid.uuid4())
        temp_path = os.path.join(os.path.dirname(file_path), random_name)
        if os.path.exists(file_path):
            shutil.move(file_path, temp_path)
            with open(temp_path, "wb") as temp_file:
                temp_file.write(os.urandom(file_size))
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.remove(temp_path)
    print(f"File '{file_path}' securely deleted with {passes} overwrite passes and randomized renaming.")
def wipe_free_space(directory):
    temp_file = os.path.join(directory, "shred_temp.dat")
    free_space = shutil.disk_usage(directory).free
    try:
        with open(temp_file, "wb") as f:
            for _ in tqdm(range(5), desc="Wiping free space", unit="chunk"):
                f.write(os.urandom(min(free_space, 500 * 1024 * 1024)))
                f.flush()
                os.fsync(f.fileno())
    except:
        pass
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
def shred_directory(directory, passes=7):
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return
    for root, _, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            overwrite_file(file_path, passes)
    try:
        shutil.rmtree(directory)
        print(f"Directory '{directory}' securely deleted.")
    except Exception as e:
        print(f"Error deleting directory: {e}")
def start():
    parser = argparse.ArgumentParser(description="Quantum-Secure File Shredder")
    parser.add_argument("target", help="Path to the file or directory to be shredded")
    parser.add_argument("--passes", type=int, default=7, help="Number of overwrite passes (default: 7)")
    parser.add_argument("--wipe-free-space", action="store_true", help="Wipe free disk space")
    args = parser.parse_args()
    if os.path.isdir(args.target):
        shred_directory(args.target, args.passes)
    elif os.path.isfile(args.target):
        overwrite_file(args.target, args.passes)
    else:
        print(f"Error: Target not found: {args.target}")
        sys.exit(1)
    if args.wipe_free_space:
        wipe_free_space(os.path.dirname(args.target))
        print("Free space wiped.")
def run_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = ctk.CTk()
    app.title("Quantum-Secure File Shredder")
    app.overrideredirect(True)
    window_width = 600
    window_height = 300
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    target_path = ctk.StringVar()
    passes_var = ctk.IntVar(value=7) 
    wipe_space_var = ctk.BooleanVar(value=False)
    def browse_file():
        file = filedialog.askopenfilename()
        if file:
            target_path.set(file)
            manual_entry.place_forget()
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            target_path.set(folder)
            manual_entry.place_forget()
    def start_shredding():
        path = target_path.get()
        wipe = wipe_space_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please select a valid file or folder.")
            return
        try:
            passes = int(passes_var.get()) if passes_var.get() != "" else 7
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Please enter a valid number of overwrite passes.")
            return
        try:
            if os.path.isdir(path):
                shred_directory(path, passes)
            elif os.path.isfile(path):
                overwrite_file(path, passes)
            else:
                messagebox.showerror("Error", f"Target not found: {path}")
                return
            if wipe:
                wipe_free_space(os.path.dirname(path))
            messagebox.showinfo("Success", "Shredding completed securely.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    bg_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="#0d0d1a")
    bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    panel = ctk.CTkFrame(bg_frame, corner_radius=20, fg_color="#1a1a2e")
    panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
    manual_entry = ctk.CTkEntry(panel, textvariable=target_path, width=400, height=35,
                                placeholder_text="Enter path manually", font=("Arial", 16))
    manual_entry.place_forget()
    select_box = ctk.CTkComboBox(
        panel,
        values=["Browse File", "Browse Folder", "Path"],
        variable=ctk.StringVar(),
        width=400,
        height=45,
        font=("Arial", 16),
    )
    select_box.set("Select File/Folder or Enter Path")
    select_box.place(relx=0.5, rely=0.1, anchor="n")
    def on_select(choice):
        if choice == "Browse File":
            manual_entry.place_forget()
            browse_file()
        elif choice == "Browse Folder":
            manual_entry.place_forget()
            browse_folder()
        elif choice == "Path":
            manual_entry.place(relx=0.5, rely=0.25, anchor="n")
            target_path.set("")
            select_box.set("Path")
    select_box.configure(command=on_select)
    passes_label = ctk.CTkLabel(panel, text="Overwrite Passes (Default 7):",
                                font=("Arial", 16), text_color="#00bfff")
    passes_label.place(relx=0.2, rely=0.4, anchor="w")
    passes_entry = ctk.CTkEntry(panel, textvariable=passes_var, width=80, height=30, font=("Arial", 16))
    passes_entry.place(relx=0.65, rely=0.4, anchor="w")
    ctk.CTkCheckBox(panel, text="🧹 Wipe Free Disk Space", variable=wipe_space_var,
                     font=("Arial", 16), fg_color="#3399ff").place(relx=0.5, rely=0.6, anchor="center")
    ctk.CTkButton(panel, text="🚀 Start Shredding", border_width=2, border_color="#3399ff",
                  command=start_shredding, width=200, height=45, corner_radius=15,
                  fg_color="#3399ff", hover_color="#2673cc", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.8, anchor="center")
    exit_button = ctk.CTkButton(bg_frame, text="🚪 Exit", width=70, height=30,
                                corner_radius=12, fg_color="#ff6666", hover_color="#ff4d4d",
                                font=("Arial", 14, "bold"), command=app.destroy)
    exit_button.place(relx=0.98, rely=0.02, anchor="ne")
    def move_window(event):
        app.geometry(f'+{event.x_root}+{event.y_root}')
    bg_frame.bind("<B1-Motion>", move_window)
    app.mainloop()
    sys.exit(0)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        start() 
    else:
        run_gui() 