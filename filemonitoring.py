import os
import time
import shutil
import logging
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Define source and destination directories
SOURCE_DIR = "./MonitoredFolder"
DEST_DIR = "./SecondFolder"

class FileMoverHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"New file detected: {event.src_path}")
            self.move_file(event.src_path)

    def move_file(self, file_path):
        """Move file after ensuring it's fully written."""
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DEST_DIR, file_name)

        # Ensure file is fully written before moving
        while True:
            try:
                initial_size = os.path.getsize(file_path)
                time.sleep(0.5)
                if os.path.getsize(file_path) == initial_size:
                    break  # File is done writing
            except FileNotFoundError:
                return  # File was removed before moving

        try:
            shutil.move(file_path, dest_path)
            logging.info(f"Moved: {file_name} → {DEST_DIR}")
        except Exception as e:
            logging.error(f"Error moving {file_name}: {e}")

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
