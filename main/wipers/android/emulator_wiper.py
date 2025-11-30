"""
@fileoverview Android Emulator Wiper

Provides wipe instructions for Android emulators. Automated wiping
is not recommended for emulators; instead, users are directed to
use the emulator's built-in wipe-data command.

@author Team PD Lovers
@version 1.0.0
"""

from common import console_ui


def send_factory_reset_command(device_profile: dict) -> None:
    """
    Display instructions for wiping an Android emulator.
    
    Emulators should be wiped using the emulator command-line
    tool with the -wipe-data flag for a clean reset.
    
    Args:
        device_profile: Device profile dictionary.
    """
    avd_name = device_profile.get('avd_name', 'Unknown_AVD')
    print("\n--> Emulator detected. Automated wiping is not recommended.")
    console_ui.print_emulator_wipe_instructions(avd_name)