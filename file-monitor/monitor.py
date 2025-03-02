import os
import time
import shutil
import logging
import redis
from datetime import datetime
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Define source and destination directories
SOURCE_DIR = os.getenv("SOURCE_DIR", "/app/MonitoredFolder")
DEST_DIR = os.getenv("DEST_DIR", "/app/SecondFolder")

# Get Redis connection details from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"New file detected: {event.src_path}")
            self.move_file(event.src_path)

    def move_file(self, file_path):
        """Move file with Redis locking to prevent conflicts."""
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DEST_DIR, file_name)
        redis_lock_key = f"lock:{file_name}"

        # Try to acquire the lock for this file
        lock_acquired = redis_client.set(redis_lock_key, "locked", nx=True, ex=10)

        if not lock_acquired:
            logging.info(f"Skipping {file_name}, already being processed by another instance.")
            return

        # Ensure file is fully written before moving
        while True:
            try:
                initial_size = os.path.getsize(file_path)
                time.sleep(0.5)
                if os.path.getsize(file_path) == initial_size:
                    break
            except FileNotFoundError:
                redis_client.delete(redis_lock_key)
                return  # File was removed before moving

        # Handle filename conflicts
        if os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(file_name)
            dest_path = os.path.join(DEST_DIR, f"{name}_{timestamp}{ext}")
            logging.info(f"File with the same name exists. Renaming to: {dest_path}")

        try:
            shutil.move(file_path, dest_path)
            logging.info(f"Moved: {file_name} → {dest_path}")
        except Exception as e:
            logging.error(f"Error moving {file_name}: {e}")

        # Release the Redis lock
        redis_client.delete(redis_lock_key)

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved: {event.src_path} → {event.dest_path}")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(SOURCE_DIR, exist_ok=True)
    os.makedirs(DEST_DIR, exist_ok=True)

    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    logging.info(f"Monitoring {SOURCE_DIR}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopping file watcher...")

    observer.join()