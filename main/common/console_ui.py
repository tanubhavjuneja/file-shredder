"""
@fileoverview Console User Interface Utilities

Provides console-based UI functions for displaying messages,
gathering user input, and showing instructions. Used as a
fallback when the GUI is not available.

@author Team PD Lovers
@version 1.0.0
"""


def get_user_confirmation(prompt_text: str, model_name: str = "this device") -> bool:
    """
    Get user confirmation via console input.
    
    Displays a warning and prompts user to type confirmation text.
    
    Args:
        prompt_text: Text the user must type to confirm.
        model_name: Device model name to display in warning.
        
    Returns:
        bool: True if user typed the correct confirmation.
    """
    print(f"\nWARNING: THIS WILL PERMANENTLY DESTROY ALL DATA ON '{model_name}'.")
    try:
        response = input(f"To proceed, type {prompt_text} and press Enter: ")
        return response.strip().upper() == prompt_text.upper()
    except KeyboardInterrupt:
        return False


def print_device_profile(profile: dict) -> None:
    """
    Display device profile information.
    
    Args:
        profile: Device profile dictionary.
    """
    print("\n--- Device Wipe Plan ---")
    for key, val in profile.items():
        print(f"  {key.replace('_', ' ').title()}: {val}")
    print("--------------------------")


def print_enable_adb_instructions() -> None:
    """Display instructions for enabling USB debugging."""
    print("ACTION REQUIRED: Enable USB Debugging in Developer Options.")


def print_authorize_device_instructions() -> None:
    """Display instructions for authorizing USB debugging."""
    print("ACTION REQUIRED: Check your phone for the 'Allow USB Debugging' popup.")


def print_offline_device_instructions() -> None:
    """Display troubleshooting steps for offline devices."""
    print("TROUBLESHOOTING: Device is Offline. Replug USB and toggle Debugging.")


def print_stage2_instructions() -> None:
    """Display Stage 2 instructions for overwrite wipe."""
    print("ACTION REQUIRED: Re-enable ADB after reset for Stage 2.")


def print_emulator_wipe_instructions(avd_name: str) -> None:
    """
    Display emulator wipe instructions.
    
    Args:
        avd_name: Name of the Android Virtual Device.
    """
    print(f"ACTION REQUIRED: Run 'emulator -avd {avd_name} -wipe-data' manually.")


def print_manufacturer_recovery_instructions(manufacturer: str = "") -> None:
    """
    Display manufacturer-specific recovery instructions.
    
    Args:
        manufacturer: Device manufacturer name.
    """
    print(f"ACTION REQUIRED: Manually select 'Wipe Data/Factory Reset' in recovery menu for {manufacturer}.")