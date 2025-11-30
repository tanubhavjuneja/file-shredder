"""
@fileoverview Background Worker Threads for SuperShredder

Provides QThread-based workers for running long-running operations
in the background without blocking the UI. Includes workers for:
- Windows file shredding operations
- Android device wiping operations
- Device connection status checking

@author Team PD Lovers
@version 1.0.0
"""

import os
import sys
import shutil
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from wipers.windows import core as windows_logic
from wipers.android import orchestrator as android_wiper
from wipers.android import device_manager


class WorkerSignals(QObject):
    """
    Defines signals for worker thread communication.
    
    Signals:
        progress: Emits an integer (0-100) for progress updates.
        log: Emits a string message for logging.
        finished: Emits (success: bool, message: str) when complete.
        canceled: Emits when the operation is canceled.
    """
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    canceled = pyqtSignal()


class WindowsShredWorker(QThread):
    """
    Background worker for Windows file shredding operations.
    
    Performs secure file deletion using encryption and multi-pass
    overwriting. Supports directories, individual files, and
    optional free space wiping.
    
    Attributes:
        signals: WorkerSignals instance for thread communication.
        targets: List of file/directory paths to shred.
        passes: Number of overwrite passes (1-35).
        wipe_free: Whether to wipe free disk space after shredding.
        chunk_size: Size of write chunks in bytes.
    """
    
    def __init__(self, targets: list, passes: int, wipe_free: bool, chunk_size: int):
        """
        Initialize the shred worker.
        
        Args:
            targets: List of file/directory paths to shred.
            passes: Number of overwrite passes.
            wipe_free: Whether to wipe free space.
            chunk_size: Size of write chunks in bytes.
        """
        super().__init__()
        self.signals = WorkerSignals()
        self.targets = targets
        self.passes = passes
        self.wipe_free = wipe_free
        self.chunk_size = chunk_size
        self._stop_requested = False

    def request_stop(self):
        """Request the worker to stop at the next safe point."""
        self._stop_requested = True

    def run(self):
        """
        Execute the shredding operation.
        
        Expands directories to individual files, shreds each file,
        removes empty directories, and optionally wipes free space.
        """
        completed_files = 0

        # Expand directories to individual file list
        all_files = []
        for target in self.targets:
            if os.path.isdir(target):
                for root, _, files in os.walk(target, topdown=False):
                    for f in files:
                        all_files.append(os.path.join(root, f))
            else:
                all_files.append(target)

        total_files = len(all_files)
        if total_files == 0:
            self.signals.finished.emit(False, "No files found.")
            return

        self.signals.log.emit(f"Starting shred. Targets: {len(self.targets)} | Total files: {total_files}")

        # Shred Loop
        for fpath in all_files:
            if self._stop_requested:
                self.signals.canceled.emit()
                return

            self.signals.log.emit(f"Shredding: {fpath}")
            try:
                # Using the new windows logic path
                windows_logic.secure_remove(fpath, self.passes, self.chunk_size)
            except Exception as e:
                self.signals.log.emit(f"Error: {e}")

            completed_files += 1
            progress = int((completed_files / total_files) * 80)
            self.signals.progress.emit(progress)

        # Remove empty directories
        for target in self.targets:
            if os.path.isdir(target):
                try:
                    shutil.rmtree(target)
                    self.signals.log.emit(f"Removed dir: {target}")
                except Exception:
                    pass

        # Wipe Free Space
        if self.wipe_free:
            self.signals.log.emit("Wiping free space...")
            for i in range(5):
                if self._stop_requested: return
                try:
                    base_dir = os.path.dirname(self.targets[0]) if self.targets else "."
                    windows_logic.wipe_free_space(base_dir, self.chunk_size)
                except:
                    pass
                self.signals.progress.emit(80 + (i + 1) * 4)

        self.signals.progress.emit(100)
        self.signals.finished.emit(True, "Operation Complete")


class AndroidWipeWorker(QThread):
    """
    Background worker for Android device wiping operations.
    
    Executes the Android wipe orchestrator in a background thread,
    redirecting stdout to emit log signals for UI display.
    
    Attributes:
        signals: WorkerSignals instance for thread communication.
        confirmation_callback: Callback function for user confirmation.
    """
    
    def __init__(self, confirmation_callback):
        """
        Initialize the Android wipe worker.
        
        Args:
            confirmation_callback: Function called to confirm wipe action.
        """
        super().__init__()
        self.signals = WorkerSignals()
        self.confirmation_callback = confirmation_callback

    def run(self):
        """
        Execute the Android wipe operation.
        
        Redirects stdout to capture log output from the orchestrator
        and emit it as log signals.
        """
        class StreamToSignal:
            """Redirects write calls to a Qt signal."""
            
            def __init__(self, signal):
                self.signal = signal

            def write(self, text):
                if text.strip():
                    self.signal.emit(text.strip())

            def flush(self):
                pass

        original_stdout = sys.stdout
        sys.stdout = StreamToSignal(self.signals.log)

        try:
            self.signals.log.emit("Initializing Android Wiper Module...")
            # Calling the new orchestrator path
            android_wiper.start(confirmation_callback=self.confirmation_callback)
            self.signals.progress.emit(100)
            self.signals.finished.emit(True, "Android Process Finished")
        except Exception as e:
            self.signals.finished.emit(False, str(e))
        finally:
            sys.stdout = original_stdout


class DeviceCheckWorker(QThread):
    """
    Background worker for checking Android device connection status.
    
    Polls ADB to detect connected devices without blocking the UI.
    Used for real-time device status updates in the Android tab.
    
    Signals:
        result: Emits (status: str, device_id: str) with connection state.
    """
    result = pyqtSignal(str, str)

    def run(self):
        """
        Check for connected Android devices via ADB.
        
        Emits the device status ('authorized', 'unauthorized', 'none', 'error')
        and device ID through the result signal.
        """
        try:
            status, device_id = device_manager.detect_device_state()
            self.result.emit(status, str(device_id))
        except Exception:
            self.result.emit('error', 'None')