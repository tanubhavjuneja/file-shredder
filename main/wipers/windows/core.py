"""
@fileoverview Windows Secure File Deletion Core

Provides military-grade secure file deletion capabilities using
AES encryption and multi-pass random data overwriting. Implements
the DoD 5220.22-M sanitization method principles.

Deletion Process:
    1. Encrypt file content with AES-256-CBC (random key/IV)
    2. Overwrite with random data for N passes
    3. Rename to random UUID to obscure original filename
    4. Delete the file

@author Team PD Lovers
@version 1.0.0
"""

import os
import shutil
import uuid
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_file_inplace(file_path: str) -> None:
    """
    Encrypt file content in-place with AES-256-CBC.
    
    Generates a random 256-bit key and 128-bit IV, encrypts the
    file content, and writes it back. The key is discarded,
    making the original content unrecoverable.
    
    Args:
        file_path: Absolute path to the file to encrypt.
    """
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, "rb") as f:
        data = f.read()

    # Pad to AES block size (16 bytes)
    if len(data) % 16 != 0:
        data += b" " * (16 - len(data) % 16)

    encrypted_data = encryptor.update(data) + encryptor.finalize()

    with open(file_path, "wb") as f:
        f.write(encrypted_data)


def secure_remove(path: str, passes: int, chunk_size: int = 1024 * 1024) -> None:
    """
    Securely delete a file using encryption and multi-pass overwriting.
    
    Performs the following steps:
    1. Encrypts file content with AES-256
    2. Overwrites with random data for the specified number of passes
    3. Renames file to random UUID (metadata obfuscation)
    4. Overwrites renamed file and deletes it
    
    Args:
        path: Absolute path to the file to delete.
        passes: Number of random data overwrite passes (1-35).
        chunk_size: Size of write chunks in bytes (default 1MB).
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    # Step 1: Encrypt file content
    encrypt_file_inplace(path)
    file_size = os.path.getsize(path)

    # Step 2: Multi-pass random overwrite
    for _ in range(passes):
        with open(path, "wb") as f:
            remaining = file_size
            while remaining > 0:
                write_size = min(chunk_size, remaining)
                f.write(os.urandom(write_size))
                f.flush()
                os.fsync(f.fileno())
                remaining -= write_size

    # Step 3: Rename and delete (metadata obfuscation)
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


def wipe_free_space(directory: str, chunk_size: int, writer_chunks: int = 5) -> None:
    """
    Fill free disk space with random data to prevent recovery of deleted files.
    
    Creates a temporary file and writes random data until disk space
    is exhausted or the specified number of chunks is written.
    The temporary file is then deleted.
    
    Args:
        directory: Directory on the target disk to wipe.
        chunk_size: Size of each write chunk in bytes.
        writer_chunks: Maximum number of chunks to write.
    """
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