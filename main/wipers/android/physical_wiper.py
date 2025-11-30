"""
@fileoverview Physical Android Device Wiper

Handles factory reset operations for physical Android devices.
Supports automated wipe for stock Android and provides manual
instructions for manufacturer-specific recovery modes.

Manual Wipe Brands:
    Vivo, Oppo, Realme, Xiaomi, Redmi - require manual recovery navigation

@author Team PD Lovers
@version 1.0.0
"""

import time
from common import adb_wrapper, console_ui

# Manufacturers requiring manual recovery mode navigation
MANUAL_WIPE_BRANDS = ['vivo', 'oppo', 'realme', 'xiaomi', 'redmi']


def _send_key_event(device_id: str, keycode: int) -> None:
    """
    Send a key event to the device via ADB.
    
    Args:
        device_id: ADB device identifier.
        keycode: Android keycode to send.
    """
    adb_wrapper.run_command(
        ['adb', '-s', device_id, 'shell', 'input', 'keyevent', str(keycode)],
        check_errors=False
    )


def _poll_for_recovery_mode(device_id: str, timeout: int = 90, interval: int = 5) -> bool:
    """
    Poll for device to enter recovery mode.
    
    Continuously checks device state until it enters recovery
    mode or timeout is reached.
    
    Args:
        device_id: ADB device identifier.
        timeout: Maximum seconds to wait.
        interval: Seconds between checks.
        
    Returns:
        bool: True if device entered recovery mode.
    """
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


def wipe_physical_device(device_profile: dict) -> None:
    """
    Execute factory reset on a physical Android device.
    
    For manufacturer-specific devices, reboots to recovery and
    provides manual instructions. For stock Android, attempts
    automated recovery wipe with fallback to menu navigation.
    
    Args:
        device_profile: Device profile dictionary.
    """
    device_id = device_profile.get('serial')
    brand = device_profile.get('brand', '').lower()

    if brand in MANUAL_WIPE_BRANDS:
        print(f"--> Manufacturer '{brand.capitalize()}' detected. Directing to manual recovery...")
        adb_wrapper.run_command(['adb', '-s', device_id, 'reboot', 'recovery'])
        console_ui.print_manufacturer_recovery_instructions(brand)
    else:
        print("--> Attempting automated wipe...")
        adb_wrapper.run_command(['adb', '-s', device_id, 'reboot', 'recovery-wipe'])

        if not _poll_for_recovery_mode(device_id):
            print("--> Device wiped automatically.")
            return

        # Fallback: navigate recovery menu
        print("--> Automated wipe failed. Attempting menu navigation...")
        _send_key_event(device_id, 20)  # KEYCODE_DPAD_DOWN
        time.sleep(1)
        _send_key_event(device_id, 20)  # KEYCODE_DPAD_DOWN
        time.sleep(1)
        _send_key_event(device_id, 66)  # KEYCODE_ENTER

        console_ui.print_manufacturer_recovery_instructions(brand)