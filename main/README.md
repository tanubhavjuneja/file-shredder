# SuperShredder

**SuperShredder** is a powerful, cross-platform security tool designed to securely erase data from Windows file systems and Android devices. Built with a modern, "hacker-style" frameless GUI using PyQt6, it ensures that deleted files are unrecoverable by utilizing military-grade encryption and multi-pass overwriting techniques.
**Self-Contained & Portable:** This tool comes with bundled ADB binaries, eliminating the need for complex system configuration. It also includes a build script to compile the application into a standalone `.exe` file.

## 🚀 Features

### 🖥️ Windows File Shredder
* **AES Encryption In-Place:** Before deletion, file content is overwritten with encrypted noise using AES (CBC mode) with a random key and IV.
* **Secure Overwrite:** Performs multiple passes of random data overwrites to ensure magnetic remanence cannot be used to recover data.
* **Metadata Obfuscation:** Renames files to random UUIDs before deletion to hide original filenames.
* **Free Space Wiping:** Fills free disk space with random data to prevent recovery of previously deleted files.

### 📱 Android Wiper
* **Smart Strategy Detection:** Automatically determines the best wiping method based on the device's Android version and encryption state.
    * **Crypto Wipe:** Used for encrypted devices (Android 6+).
    * **Factory Reset/Overwrite:** Used for older devices or emulators.
* **Device Management:** Auto-detects device states (Authorized, Unauthorized, Offline) and guides the user through ADB connection steps.
* **Emulator Support:** Detects if the connected device is an emulator and adjusts the wiping command accordingly.

### 🎨 User Interface
* **Modern Dark Theme:** Custom-styled, frameless window with a translucent background and rounded corners.
* **Easy Navigation:** Sidebar navigation to switch between Windows and Android modules.
* **Integrated Controls:** Custom minimize and exit buttons integrated into the UI.

---

## 🛠️ Installation

### Prerequisites
* Python 3.x

### Steps
1.  **Clone the repository**
    ```bash
    git clone https://github.com/tanubhavjuneja/file-shredder
    cd file-shredder/main
    ```

2.  **Install Dependencies**
    Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    You have two options to run SuperShredder:

Option A: Run from Source Launch the application directly using Python:  
   ```bash
   python main.py
   ```   
    
Option B: Build Standalone Executable. Use the provided build script to create a portable .exe file. This will bundle all dependencies and the ADB binaries into a single file.
   ```bash
   python build.py
   ```

The build script checks for adb.exe and DLLs in the bin/ folder and bundles them.
Once finished, the executable will be available at: dist/SuperShredder.exe
   

---

## 📖 Usage

### Windows Tab
1.  Select the **File Shredder** tab from the sidebar.
2.  Choose the file or directory you wish to shred.
3.  The application will encrypt the content, overwrite it multiple times, rename the file, and finally delete it.

### Android Tab
1.  Connect your Android device via USB and ensure **USB Debugging** is enabled.
2.  Select the **Android Wiper** tab.
3.  The tool will detect your device. If authorized, it will display the device profile.
4.  Click to start the wipe. The tool will execute the appropriate strategy (Crypto Wipe or Factory Reset).

---

## 🏗️ Project Structure

```text
SuperShredder/
├── main.py                 # Application entry point & Main Window UI
├── build.py                # PyInstaller build script for creating .exe
├── requirements.txt        # Python dependencies
├── gui/                    # UI Components
│   ├── theme.py            # Stylesheets
│   └── tabs/               # Individual tab layouts (Windows/Android)
├── wipers/                 # Core Logic
│   ├── windows/
│   │   └── core.py         # Windows encryption & deletion logic
│   └── android/
│       ├── orchestrator.py # Android process manager
│       ├── strategies.py   # Wipe strategy logic
│       ├── physical_wiper.py
│       └── emulator_wiper.py
├── bin/                    # Bundled ADB binaries (adb.exe, AdbWinApi.dll, etc.)
└── common/                 # Shared utilities

```
---
## ⚠️ Disclaimer
SuperShredder is a destructive tool. Files deleted with this tool cannot be recovered. The Android wiper may perform a factory reset on connected devices. The developers are not responsible for any data loss or damage caused by the misuse of this software. Use with caution.
