import os
import random
import time
import traceback
from django.conf import settings

# This function contains the actual logic for overwriting file content.
# It is designed to run synchronously for debugging, but will be called
# asynchronously via Celery when fully configured.
def process_target(target_path, passes=7, chunk_size_mb=100, wipe_free=False):
    """
    Simulates secure data shredding by overwriting the target file multiple times
    with random data.

    Args:
        target_path (str): The absolute path to the file or directory.
        passes (int): Number of overwrites (e.g., 7 for DoD 5220.22-M standard).
        chunk_size_mb (int): Size of data chunks to write at a time (in MB).
        wipe_free (bool): If True, free space on the drive is also wiped (not implemented here).
    """

    # 1. Validation and Setup
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target path not found: {target_path}")

    if not os.path.isfile(target_path):
        # We are only simulating file shredding for now.
        raise IsADirectoryError(f"Target is a directory, not a file: {target_path}")

    file_size = os.path.getsize(target_path)
    chunk_size = chunk_size_mb * 1024 * 1024  # Convert MB to bytes

    print(f"\n--- Starting Shredding Simulation for: {target_path} ---")
    print(f"Size: {file_size} bytes, Passes: {passes}, Chunk Size: {chunk_size_mb} MB")

    try:
        # 2. Overwriting Passes
        for i in range(1, passes + 1):
            print(f"Pass {i}/{passes}: Overwriting content...")

            # Open the file in read+write binary mode ('r+b')
            with open(target_path, 'r+b') as f:
                # Seek to the beginning of the file
                f.seek(0)

                # Overwrite the file content
                bytes_written = 0
                while bytes_written < file_size:
                    # Determine the size of the chunk to write
                    write_size = min(chunk_size, file_size - bytes_written)

                    # Generate a chunk of random binary data
                    random_data = os.urandom(write_size)

                    # Write the random data chunk
                    f.write(random_data)

                    bytes_written += write_size

                # Ensure the new data is flushed to disk before closing the pass
                f.flush()
                os.fsync(f.fileno())

        # 3. Final Step: Rename and Delete
        print("Pass 8/8: Renaming and deleting file...")
        
        # Simulate renaming the file to random names before final delete
        base_dir = os.path.dirname(target_path)
        original_filename = os.path.basename(target_path)
        
        for _ in range(5):  # Rename 5 times
            random_name = ''.join(random.choices('0123456789abcdef', k=16))
            temp_path = os.path.join(base_dir, random_name)
            os.rename(target_path, temp_path)
            target_path = temp_path
            time.sleep(0.01) # Small delay for simulation

        # Final deletion
        os.remove(target_path)
        print(f"Successfully shredded and deleted file: {original_filename}")
        
        return {"status": "success", "message": f"Successfully shredded and deleted {original_filename}"}

    except Exception as e:
        # CRITICAL DEBUGGING: Print the error type and message directly.
        print(f"CORE ERROR TYPE: {type(e).__name__}")
        print(f"CORE ERROR MESSAGE: {e}")
        traceback.print_exc()
        raise # Re-raise the exception to be caught by the view.

    # Wipe free space logic (not implemented)
    if wipe_free:
        print("Wiping free space... (Simulation skipped)")
        pass
