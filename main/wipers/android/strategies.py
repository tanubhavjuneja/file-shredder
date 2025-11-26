import re
from common import console_ui
from . import physical_wiper, emulator_wiper

def determine_wipe_strategy(profile):
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

def _get_confirmation(callback, model_name, prompt="ERASE"):
    if callback:
        return callback(model_name)
    else:
        return console_ui.get_user_confirmation(prompt, model_name)

def perform_crypto_wipe(device_id, device_profile, confirmation_callback=None):
    model_name = device_profile.get('model', 'this device')
    is_emulator = device_profile.get('is_emulator', False)

    if _get_confirmation(confirmation_callback, model_name):
        if is_emulator:
            emulator_wiper.send_factory_reset_command(device_profile)
        else:
            physical_wiper.wipe_physical_device(device_profile)
    else:
        print("\nCANCELLED: User did not confirm.")

def perform_overwrite_wipe_stage1(device_id, device_profile, confirmation_callback=None):
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