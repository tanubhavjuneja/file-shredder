"""
@fileoverview PyInstaller Build Script for SuperShredder

Compiles the SuperShredder application into a standalone Windows
executable using PyInstaller. Bundles all dependencies including
the ADB binaries for a zero-dependency portable application.

Output:
    dist/SuperShredder.exe - Single-file portable executable

Requirements:
    - bin/adb.exe
    - bin/AdbWinApi.dll
    - bin/AdbWinUsbApi.dll
    - icon.ico (optional)

@author Team PD Lovers
@version 1.0.0
"""

import PyInstaller.__main__
import os


def build() -> None:
    """
    Build the SuperShredder executable.
    
    Validates required ADB binaries exist, configures PyInstaller
    options, and compiles the application into a single .exe file.
    """
    bin_folder = "bin"
    icon_filename = "icon.ico"

    # Validate required ADB binaries
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

    # Configure icon if available
    icon_args = []
    if os.path.exists(icon_filename):
        print(f"Applying icon: {icon_filename}")
        icon_args = [f'--icon={icon_filename}']
    else:
        print("Warning: 'icon.ico' not found. Building with default icon.")

    print("--- Starting Build Process ---")

    # Configure binary bundling (format: source_path;dest_folder)
    add_binary_args = [
        f'--add-binary={os.path.join(bin_folder, "adb.exe")};{bin_folder}',
        f'--add-binary={os.path.join(bin_folder, "AdbWinApi.dll")};{bin_folder}',
        f'--add-binary={os.path.join(bin_folder, "AdbWinUsbApi.dll")};{bin_folder}',
    ]

    # Run PyInstaller with configured options
    PyInstaller.__main__.run([
        'main.py',
        '--name=SuperShredder',
        '--onefile',
        '--noconsole',
        '--clean',
        *icon_args,
        *add_binary_args,
        '--hidden-import=PyQt6',
        '--hidden-import=cryptography',
    ])

    print("\n--- Build Complete ---")
    print(f"Your executable is located in: {os.path.join(os.getcwd(), 'dist', 'SuperShredder.exe')}")


if __name__ == "__main__":
    build()