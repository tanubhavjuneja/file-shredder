import os
import shutil
import sys
import uuid
import logging
from tqdm import tqdm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# ---------------- Logger Setup ---------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("DiskWiper")


# ---------------- Encryption Utility ---------------- #
def encrypt_chunk(data, key, iv):
    """Encrypt a block of data with AES-256-CBC."""
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad to 16 bytes
    if len(data) % 16 != 0:
        data += b" " * (16 - len(data) % 16)
    return encryptor.update(data) + encryptor.finalize()


# ---------------- Disk Wiper ---------------- #
def wipe_free_space(drive_root, passes=3, chunk_size=512 * 1024 * 1024):
    """
    Securely wipe free disk space by filling it with patterns and encrypted data.
    
    Args:
        drive_root (str): Path to the drive root (e.g., 'C:\\' on Windows or '/' on Linux).
        passes (int): Number of overwrite passes.
        chunk_size (int): Write size in bytes (default: 512MB).
    """
    logger.info(f"Starting secure free space wipe on: {drive_root}")
    total_free = shutil.disk_usage(drive_root).free
    logger.info(f"Total free space detected: {total_free // (1024**3)} GB")

    patterns = [
        (b"\x00", "zeros"),
        (b"\xFF", "ones"),
        (None, "random"),
        ("encrypted", "AES-256 encrypted random data"),
    ]

    for p in range(passes):
        logger.info(f"=== Pass {p+1}/{passes} ===")
        file_index = 0
        temp_files = []

        for pattern, label in patterns:
            logger.info(f"Writing pass pattern: {label}")

            try:
                while True:
                    temp_path = os.path.join(drive_root, f"shred_temp_{p}_{file_index}.dat")
                    file_index += 1
                    temp_files.append(temp_path)
                    with open(temp_path, "wb") as f:
                        written = 0
                        pbar = tqdm(total=total_free, unit="B", unit_scale=True, desc=f"Filling {label}")

                        while written < total_free:
                            ...
                            written += len(chunk)
                            pbar.update(len(chunk))

                        pbar.close()
                        logger.info(f"Temp file {temp_path} size: {written // (1024**3)} GB ({written} bytes)")

                    with open(temp_path, "wb") as f:
                        written = 0
                        pbar = tqdm(total=total_free, unit="B", unit_scale=True, desc=f"Filling {label}")

                        while written < total_free:
                            if pattern == "encrypted":
                                key = os.urandom(32)
                                iv = os.urandom(16)
                                data = os.urandom(chunk_size)
                                chunk = encrypt_chunk(data, key, iv)
                            elif pattern is None:
                                chunk = os.urandom(chunk_size)
                            else:
                                chunk = pattern * chunk_size

                            try:
                                f.write(chunk)
                                f.flush()
                                os.fsync(f.fileno())
                            except OSError:
                                # Out of space
                                break

                            written += len(chunk)
                            pbar.update(len(chunk))

                        pbar.close()

            except OSError:
                logger.warning("Disk is full for this pattern.")
            finally:
                # Delete temporary files to free space for next pass
                logger.info("Cleaning up temporary files...")
                for tf in temp_files:
                    try:
                        if os.path.exists(tf):
                            os.remove(tf)
                    except Exception as e:
                        logger.error(f"Failed to remove {tf}: {e}")
                temp_files.clear()

    logger.info("✅ Free space wiping completed successfully.")


# ---------------- CLI Entry ---------------- #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python disk_wiper.py <drive_root> [passes]")
        print("Example (Windows): python disk_wiper.py C:\\ 3")
        print("Example (Linux):   sudo python3 disk_wiper.py / 3")
        sys.exit(1)

    drive_root = sys.argv[1]
    passes = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    wipe_free_space(drive_root, passes=passes)
