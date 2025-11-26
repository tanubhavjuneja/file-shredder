from common import adb_wrapper

def detect_device_state():
    """Detects the state of a connected Android device."""
    print("--> Checking for connected devices...")
    stdout, _ = adb_wrapper.run_command(['adb', 'devices'])
    lines = stdout.strip().split('\n')[1:]
    if not lines or not lines[0]:
        return 'none', None

    try:
        device_id, state = lines[0].split()
        if state == 'device':
            print(f"--> Found authorized device: {device_id}")
            return 'authorized', device_id
        elif state == 'unauthorized':
            print(f"--> Found unauthorized device: {device_id}")
            return 'unauthorized', device_id
        elif state == 'offline':
            print(f"--> Found offline device: {device_id}")
            return 'offline', device_id
        else:
            return 'none', None
    except (ValueError, IndexError):
        return 'none', None

def profile_device(device_id):
    """Gathers key information about the device."""
    print("\n--> Profiling device...")

    def get_prop(prop_name):
        stdout, _ = adb_wrapper.run_command(['adb', '-s', device_id, 'shell', 'getprop', prop_name])
        return stdout

    storage_command = "df -h | grep /data | awk '{print $2}'"

    profile_data = {
        'model': get_prop('ro.product.model'),
        'brand': get_prop('ro.product.brand'),
        'android_version': get_prop('ro.build.version.release'),
        'serial': device_id,
        'storage_size': adb_wrapper.run_command(['adb', '-s', device_id, 'shell', storage_command])[0],
        'crypto_state': get_prop('ro.crypto.state'),
        'is_emulator': get_prop('ro.kernel.qemu') == '1',
        'avd_name': get_prop('ro.boot.qemu.avd_name')
    }
    print("--> Profile complete.")
    return profile_data