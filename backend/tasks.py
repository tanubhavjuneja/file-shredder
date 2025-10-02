# shredder/backend/tasks.py

from backend.celery import app
from .shred_core import process_target # FIXED: Use relative import

# This function is used for basic Celery health checks
@app.task
def debug_task():
    print('Request: Hello from the debug task!')


# The main task definition
@app.task(bind=True)
def secure_shred_task(self, target_path, passes, chunk_size_mb, wipe_free):
    """
    Celery task wrapper for the core shredding logic.
    
    When run synchronously (during debugging), it executes process_target immediately.
    When run asynchronously (production), it allows for status updates via 'self'.
    """
    try:
        # Call the core logic, passing the task object 'self' if it's available
        result = process_target(
            target_path=target_path,
            passes=passes,
            chunk_size_mb=chunk_size_mb,
            wipe_free=wipe_free,
            task=self # Pass the Celery task object for status updates
        )
        return result
    except FileNotFoundError as e:
        # Handle a specific expected error
        return {"status": "Error", "message": str(e)}
    except Exception as e:
        # Re-raise all other unexpected errors
        raise self.retry(exc=e, countdown=5, max_retries=3) # Retry mechanism for Celery
