import subprocess
import sys
import os


def get_adb_path():
    """
    Returns the path to the adb executable.
    It checks the 'bin' folder in both the frozen state (exe) and development state (source).
    """
    if hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller Bundle (.exe)
        # We mapped the files to the 'bin' folder inside the bundle
        base_path = sys._MEIPASS
    else:
        # Running from Source (Editor/Terminal)
        # This file is in 'common/', so we go up one level to root, then into 'bin'
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    adb_path = os.path.join(base_path, 'bin', 'adb.exe')

    # Fallback: If local bin/adb.exe is missing, try system PATH
    if not os.path.exists(adb_path):
        return 'adb'

    return adb_path


def run_command(command, check_errors=True):
    """
    Executes a shell command and returns its stdout and stderr.
    """
    cmd_list = list(command)

    # If the command starts with 'adb', replace it with the correct modular path
    if cmd_list[0] == 'adb':
        cmd_list[0] = get_adb_path()

    try:
        # Determine startup info to hide the console window on Windows
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
    except Exception as e:
        raise e