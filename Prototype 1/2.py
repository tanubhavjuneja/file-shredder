import os
import argparse
import random
import shutil
import sys
import time
import uuid
from tqdm import tqdm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# ---------------- Existing Shredder Functions (UNCHANGED) ---------------- #

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

# ---------------- CustomTkinter GUI Interface ---------------- #

import customtkinter as ctk
from tkinter import filedialog, messagebox

def run_gui():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Quantum-Secure File Shredder")
    app.geometry("600x350")

    # Variables
    target_path = ctk.StringVar()
    passes_var = ctk.IntVar(value=7)
    wipe_space_var = ctk.BooleanVar(value=False)

    def browse_file():
        file = filedialog.askopenfilename()
        if file:
            target_path.set(file)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            target_path.set(folder)

    def start_shredding():
        path = target_path.get()
        passes = passes_var.get()
        wipe = wipe_space_var.get()

        if not path:
            messagebox.showerror("Error", "Please select a file or folder.")
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

    # UI Layout
    frame = ctk.CTkFrame(app, corner_radius=15)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Quantum-Secure File Shredder", font=("Arial", 20, "bold")).pack(pady=10)

    path_entry = ctk.CTkEntry(frame, textvariable=target_path, width=400, placeholder_text="Select file or folder")
    path_entry.pack(pady=5)

    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(pady=5)
    ctk.CTkButton(button_frame, text="Browse File", command=browse_file).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Browse Folder", command=browse_folder).pack(side="left", padx=5)

    passes_frame = ctk.CTkFrame(frame)
    passes_frame.pack(pady=10)
    ctk.CTkLabel(passes_frame, text="Overwrite Passes:").pack(side="left", padx=5)
    ctk.CTkEntry(passes_frame, textvariable=passes_var, width=80).pack(side="left", padx=5)

    ctk.CTkCheckBox(frame, text="Wipe Free Disk Space", variable=wipe_space_var).pack(pady=5)

    ctk.CTkButton(frame, text="Start Shredding",border_width=2, border_color="white", command=start_shredding).pack(pady=15)

    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start()  # CLI mode
    else:
        run_gui()  # GUI mode