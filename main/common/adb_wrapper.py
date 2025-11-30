"""
@fileoverview ADB Command Wrapper

Provides a unified interface for executing ADB commands.
Automatically resolves the correct ADB executable path for
both development and PyInstaller bundled environments.

Features:
    - Auto-detection of bundled ADB in bin/ folder
    - Fallback to system PATH if local ADB not found
    - Hidden console window on Windows
    - Consistent error handling

@author Team PD Lovers
@version 1.0.0
"""

import subprocess
import sys
import os


def get_adb_path() -> str:
    """
    Resolve the path to the ADB executable.
    
    Checks for ADB in the bundled bin/ folder first (for both
    PyInstaller builds and development), then falls back to
    system PATH.
    
    Returns:
        str: Absolute path to adb.exe or 'adb' for system PATH.
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller bundle: look in extracted temp folder
        base_path = sys._MEIPASS
    else:
        # Development: look relative to this file's parent directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    adb_path = os.path.join(base_path, 'bin', 'adb.exe')

    # Fallback to system PATH if local ADB not found
    if not os.path.exists(adb_path):
        return 'adb'

    return adb_path


def run_command(command: list, check_errors: bool = True) -> tuple:
    """
    Execute an ADB command and return its output.
    
    Automatically substitutes 'adb' in the command with the
    correct local path. Hides console window on Windows.
    
    Args:
        command: Command as list of strings (e.g., ['adb', 'devices']).
        check_errors: Whether to raise exceptions on non-zero exit.
        
    Returns:
        tuple: (stdout, stderr) as stripped strings.
        
    Raises:
        RuntimeError: If command fails and check_errors is True.
        FileNotFoundError: If ADB executable is not found.
    """
    cmd_list = list(command)

    # Replace 'adb' with the resolved path
    if cmd_list[0] == 'adb':
        cmd_list[0] = get_adb_path()

    try:
        # Hide console window on Windows
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        process = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        stdout, stderr = process.communicate()

        if check_errors and process.returncode != 0:
            raise RuntimeError(f"ADB Command failed: {stderr.strip()}")

        return stdout.strip(), stderr.strip()

    except FileNotFoundError:
        raise FileNotFoundError(f"Command not found: {cmd_list[0]}. Check your 'bin' folder.")