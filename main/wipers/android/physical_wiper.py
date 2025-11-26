import time
from common import adb_wrapper, console_ui

MANUAL_WIPE_BRANDS = ['vivo', 'oppo', 'realme', 'xiaomi', 'redmi']


def _send_key_event(device_id, keycode):
    adb_wrapper.run_command(
        ['adb', '-s', device_id, 'shell', 'input', 'keyevent', str(keycode)],
        check_errors=False
    )


def _poll_for_recovery_mode(device_id, timeout=90, interval=5):
    print(f"--> Watching for device '{device_id}' for up to {timeout} seconds...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        stdout, _ = adb_wrapper.run_command(['adb', 'devices'], check_errors=False)
        lines = stdout.strip().split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) == 2 and parts[0] == device_id and parts[1] == 'recovery':
                return True
        time.sleep(interval)
    return False


def wipe_physical_device(device_profile):
    device_id = device_profile.get('serial')
    brand = device_profile.get('brand', '').lower()

    if brand in MANUAL_WIPE_BRANDS:
        print(f"--> Manufacturer '{brand.capitalize()}' detected. Directing to manual recovery...")
        adb_wrapper.run_command(['adb', '-s', device_id, 'reboot', 'recovery'])
        console_ui.print_manufacturer_recovery_instructions(brand)
    else:
        print(f"--> Attempting automated wipe...")
        adb_wrapper.run_command(['adb', '-s', device_id, 'reboot', 'recovery-wipe'])

        if not _poll_for_recovery_mode(device_id):
            print("--> Device wiped automatically.")
            return

        print("--> Automated wipe failed. Attempting menu navigation...")
        # Fallback sequence
        _send_key_event(device_id, 20)  # Down
        time.sleep(1)
        _send_key_event(device_id, 20)  # Down
        time.sleep(1)
        _send_key_event(device_id, 66)  # Enter

        console_ui.print_manufacturer_recovery_instructions(brand)