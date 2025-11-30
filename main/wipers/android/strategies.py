"""
@fileoverview Android Wipe Strategy Module

Determines and executes the appropriate wipe strategy based on
device capabilities. Supports crypto wipe for encrypted devices
and overwrite wipe for older/unencrypted devices.

@author Team PD Lovers
@version 1.0.0
"""

import re
from common import console_ui
from . import physical_wiper, emulator_wiper


def determine_wipe_strategy(profile: dict) -> str:
    """
    Determine the appropriate wipe strategy for a device.
    
    Selects 'crypto' wipe for encrypted Android 6+ devices,
    'overwrite' wipe for emulators and older/unencrypted devices.
    
    Args:
        profile: Device profile dictionary from device_manager.
        
    Returns:
        str: Either 'crypto' or 'overwrite'.
    """
    try:
        if profile.get('is_emulator'):
            return 'overwrite'

        version_str = profile.get('android_version', '')
        match = re.match(r'(\d+)', version_str)
        version_major = int(match.group(1)) if match else 0

        if version_major >= 6 and profile.get('crypto_state') == 'encrypted':
            return 'crypto'
        return 'overwrite'
    except (ValueError, TypeError, AttributeError):
        return 'overwrite'


def _get_confirmation(callback, model_name: str, prompt: str = "ERASE") -> bool:
    """
    Get user confirmation for wipe operation.
    
    Uses the provided callback if available, otherwise falls back
    to console-based confirmation.
    
    Args:
        callback: Optional confirmation callback function.
        model_name: Device model name to display.
        prompt: Confirmation prompt text.
        
    Returns:
        bool: True if user confirmed, False otherwise.
    """
    if callback:
        return callback(model_name)
    else:
        return console_ui.get_user_confirmation(prompt, model_name)


def perform_crypto_wipe(device_id: str, device_profile: dict, confirmation_callback=None) -> None:
    """
    Execute crypto wipe strategy for encrypted devices.
    
    For encrypted devices, factory reset is sufficient since the
    encryption key is destroyed, making data unrecoverable.
    
    Args:
        device_id: ADB device identifier.
        device_profile: Device profile dictionary.
        confirmation_callback: Optional confirmation callback.
    """
    model_name = device_profile.get('model', 'this device')
    is_emulator = device_profile.get('is_emulator', False)

    if _get_confirmation(confirmation_callback, model_name):
        if is_emulator:
            emulator_wiper.send_factory_reset_command(device_profile)
        else:
            physical_wiper.wipe_physical_device(device_profile)
    else:
        print("\nCANCELLED: User did not confirm.")


def perform_overwrite_wipe_stage1(device_id: str, device_profile: dict, confirmation_callback=None) -> None:
    """
    Execute overwrite wipe strategy for unencrypted devices.
    
    For unencrypted devices, performs factory reset and instructs
    user to complete Stage 2 (fill storage with random data).
    
    Args:
        device_id: ADB device identifier.
        device_profile: Device profile dictionary.
        confirmation_callback: Optional confirmation callback.
    """
    model_name = device_profile.get('model', 'this device')
    is_emulator = device_profile.get('is_emulator', False)

    if _get_confirmation(confirmation_callback, model_name):
        if is_emulator:
            emulator_wiper.send_factory_reset_command(device_profile)
        else:
            physical_wiper.wipe_physical_device(device_profile)
            console_ui.print_stage2_instructions()
    else:
        print("\nCANCELLED: User did not confirm.")