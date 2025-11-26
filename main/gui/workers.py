import os
import sys
import shutil
from PyQt6.QtCore import QThread, pyqtSignal, QObject

# NEW IMPORTS: Refecting the structure change
from wipers.windows import core as windows_logic
from wipers.android import orchestrator as android_wiper
from wipers.android import device_manager


class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    canceled = pyqtSignal()


class WindowsShredWorker(QThread):
    def __init__(self, targets, passes, wipe_free, chunk_size):
        super().__init__()
        self.signals = WorkerSignals()
        self.targets = targets
        self.passes = passes
        self.wipe_free = wipe_free
        self.chunk_size = chunk_size
        self._stop_requested = False

    def request_stop(self):
        self._stop_requested = True

    def run(self):
        completed_files = 0

        # Expand directories
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
    def __init__(self, confirmation_callback):
        super().__init__()
        self.signals = WorkerSignals()
        self.confirmation_callback = confirmation_callback

    def run(self):
        class StreamToSignal:
            def __init__(self, signal):
                self.signal = signal

            def write(self, text):
                if text.strip():
                    self.signal.emit(text.strip())

            def flush(self): pass

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
    result = pyqtSignal(str, str)

    def run(self):
        try:
            status, device_id = device_manager.detect_device_state()
            self.result.emit(status, str(device_id))
        except Exception:
            self.result.emit('error', 'None')