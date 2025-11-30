"""
@fileoverview Android Wipe Orchestrator

Main entry point for the Android wiping module. Coordinates device
detection, strategy selection, and wipe execution based on device
state and capabilities.

Wipe Strategies:
    - Crypto Wipe: For encrypted devices (Android 6+)
    - Overwrite Wipe: For older/unencrypted devices and emulators

@author Team PD Lovers
@version 1.0.0
"""

from common import console_ui
from . import device_manager, strategies


def start(confirmation_callback=None):
    """
    Main entry point for the Android wiping module.
    
    Detects connected devices, determines appropriate wipe strategy,
    and executes the wipe operation based on device capabilities.
    
    Args:
        confirmation_callback: Optional callback for user confirmation.
            If provided, called with device model name. Should return
            True to proceed with wipe, False to cancel.
    """
    # Detect device connection state
    state, device_id = device_manager.detect_device_state()

    if state == 'authorized':
        # Profile device and determine wipe strategy
        device_profile = device_manager.profile_device(device_id)
        strategy = strategies.determine_wipe_strategy(device_profile)

        console_ui.print_device_profile(device_profile)

        # Execute appropriate wipe strategy
        if strategy == 'crypto':
            strategies.perform_crypto_wipe(device_id, device_profile, confirmation_callback)
        else:
            strategies.perform_overwrite_wipe_stage1(device_id, device_profile, confirmation_callback)

    elif state == 'unauthorized':
        console_ui.print_authorize_device_instructions()
    elif state == 'offline':
        console_ui.print_offline_device_instructions()
    else:
        console_ui.print_enable_adb_instructions()