from common import console_ui

def send_factory_reset_command(device_profile):
    """
    Instructions for manual emulator wiping.
    """
    avd_name = device_profile.get('avd_name', 'Unknown_AVD')
    print("\n--> Emulator detected. Automated wiping is not recommended.")
    console_ui.print_emulator_wipe_instructions(avd_name)