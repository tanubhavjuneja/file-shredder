import PyInstaller.__main__
import os
import sys


def build():
    # Define the modular folder name
    bin_folder = "bin"
    # Define your icon file name here
    icon_filename = "icon.ico"

    # Check if files exist in the modular 'bin' folder
    required_files = ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll"]
    missing = []

    for f in required_files:
        file_path = os.path.join(bin_folder, f)
        if not os.path.exists(file_path):
            missing.append(file_path)

    if missing:
        print(f"Error: Missing files in the '{bin_folder}' folder!")
        print(f"Please move the ADB files into the '{bin_folder}' directory.")
        print(f"Missing: {', '.join(missing)}")
        return

    # Check for Icon
    icon_args = []
    if os.path.exists(icon_filename):
        print(f"Applying icon: {icon_filename}")
        icon_args = [f'--icon={icon_filename}']
    else:
        print("Warning: 'icon.ico' not found. Building with default icon.")

    print("--- Starting Build Process ---")

    # The syntax for adding binaries is "source_path;dest_folder"
    add_binary_args = [
        f'--add-binary={os.path.join(bin_folder, "adb.exe")};{bin_folder}',
        f'--add-binary={os.path.join(bin_folder, "AdbWinApi.dll")};{bin_folder}',
        f'--add-binary={os.path.join(bin_folder, "AdbWinUsbApi.dll")};{bin_folder}',
    ]

    PyInstaller.__main__.run([
        'main.py',
        '--name=SuperShredder',
        '--onefile',
        '--noconsole',
        '--clean',

        # Add Icon Argument
        *icon_args,

        # Add our modular binaries
        *add_binary_args,

        # Hidden imports to ensure stability
        '--hidden-import=PyQt6',
        '--hidden-import=cryptography',
    ])

    print("\n--- Build Complete ---")
    print(f"Your executable is located in: {os.path.join(os.getcwd(), 'dist', 'SuperShredder.exe')}")


if __name__ == "__main__":
    build()