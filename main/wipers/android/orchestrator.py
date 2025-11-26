from common import console_ui
from . import device_manager, strategies

def start(confirmation_callback=None):
    """
    Main entry point for the Android wiping module.
    """
    # 1. Detect the device and its connection state.
    state, device_id = device_manager.detect_device_state()

    # 2. Decide what to do based on the device's state.
    if state == 'authorized':
        device_profile = device_manager.profile_device(device_id)
        strategy = strategies.determine_wipe_strategy(device_profile)

        console_ui.print_device_profile(device_profile)

        if strategy == 'crypto':
            strategies.perform_crypto_wipe(device_id, device_profile, confirmation_callback)
        else:  # strategy == 'overwrite'
            strategies.perform_overwrite_wipe_stage1(device_id, device_profile, confirmation_callback)

    elif state == 'unauthorized':
        console_ui.print_authorize_device_instructions()
    elif state == 'offline':
        console_ui.print_offline_device_instructions()
    else:  # state == 'none'
        console_ui.print_enable_adb_instructions()