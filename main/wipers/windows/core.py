import os
import shutil
import uuid
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_file_inplace(file_path: str):
    """Overwrites file content with encrypted noise."""
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as f:
        data = f.read()

    if len(data) % 16 != 0:
        data += b" " * (16 - len(data) % 16)

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(file_path, "wb") as f:
        f.write(encrypted_data)


def secure_remove(path: str, passes: int, chunk_size: int = 1024 * 1024):
    """Performs multi-pass overwrite and secure deletion."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    encrypt_file_inplace(path)
    file_size = os.path.getsize(path)

    for _ in range(passes):
        with open(path, "wb") as f:
            remaining = file_size
            while remaining > 0:
                write_size = min(chunk_size, remaining)
                f.write(os.urandom(write_size))
                f.flush()
                os.fsync(f.fileno())
                remaining -= write_size

    dir_name = os.path.dirname(path) or "."
    for _ in range(passes):
        random_name = os.path.join(dir_name, str(uuid.uuid4()))
        if os.path.exists(path):
            try:
                shutil.move(path, random_name)
                with open(random_name, "wb") as tf:
                    tf.write(os.urandom(min(file_size, 4096)))
                os.remove(random_name)
            except FileNotFoundError:
                pass


def wipe_free_space(directory: str, chunk_size: int, writer_chunks=5):
    """Creates a temporary file to fill disk space."""
    temp_file = os.path.join(directory, "shred_temp.dat")
    try:
        free_space = shutil.disk_usage(directory).free
        with open(temp_file, "wb") as f:
            for _ in range(writer_chunks):
                write_size = min(free_space, chunk_size)
                if write_size <= 0: break
                chunk = os.urandom(write_size)
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
                free_space -= write_size
    except Exception:
        pass
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass