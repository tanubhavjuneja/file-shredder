"""
This module handles all console-based user interface elements.
"""

def get_user_confirmation(prompt_text, model_name="this device"):
    print(f"\nWARNING: THIS WILL PERMANENTLY DESTROY ALL DATA ON '{model_name}'.")
    try:
        response = input(f"To proceed, type {prompt_text} and press Enter: ")
        return response.strip().upper() == prompt_text.upper()
    except KeyboardInterrupt:
        return False

def print_device_profile(profile):
    print("\n--- Device Wipe Plan ---")
    for key, val in profile.items():
        print(f"  {key.replace('_', ' ').title()}: {val}")
    print("--------------------------")

def print_enable_adb_instructions():
    print("ACTION REQUIRED: Enable USB Debugging in Developer Options.")

def print_authorize_device_instructions():
    print("ACTION REQUIRED: Check your phone for the 'Allow USB Debugging' popup.")

def print_offline_device_instructions():
    print("TROUBLESHOOTING: Device is Offline. Replug USB and toggle Debugging.")

def print_stage2_instructions():
    print("ACTION REQUIRED: Re-enable ADB after reset for Stage 2.")

def print_emulator_wipe_instructions(avd_name):
    print(f"ACTION REQUIRED: Run 'emulator -avd {avd_name} -wipe-data' manually.")

def print_manufacturer_recovery_instructions(manufacturer=""):
    print(f"ACTION REQUIRED: Manually select 'Wipe Data/Factory Reset' in recovery menu for {manufacturer}.")