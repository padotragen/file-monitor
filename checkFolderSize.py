from genericpath import getsize
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Get source and destination directories from environment variables
SOURCE_DIR = os.getenv("SOURCE_DIR", "/app/MonitoredFolder")
RUMBAFOLDER= "/Users/w.wrightg/Documents/Python/File Monitoring/SecondFolder"
MAXFOLDERSIZE = 2
TARGETFOLDERSIZE = 1

class FolderCleanup:
    def __init__(self, directory):
        if not os.path.exists(directory):
            raise ValueError(f"Path '{directory}' does not exist.")
        if not os.path.isdir(directory):
            raise ValueError(f"Path '{directory}' is not a directory.")
        
        self.directory = directory
    
    def get_dir_size(self):
        """Calculate the total size of files in the directory recursively."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Skip if it is a symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size
    
    def get_files_by_oldest(self):
        """Return a list of files sorted by modification time (oldest first)."""
        files = [os.path.join(self.directory, f) for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        return sorted(files, key=os.path.getmtime)
    
    def remove_files_until_size(self, target_size_mb):
        """Remove the oldest files until the directory size is at or below the target size (in MB)."""
        target_size_bytes = target_size_mb * 1024 * 1024
        current_size = self.get_dir_size()
        
        if current_size <= target_size_bytes:
            logging.info(f"Directory size is already at or below target size ({target_size_mb} MB).")
            return
        
        files = self.get_files_by_oldest()
        
        for file_path in files:
            if current_size <= target_size_bytes:
                break
            file_size = os.path.getsize(file_path)
            os.remove(file_path)
            current_size -= file_size
            logging.info(f"Removed: {file_path}, Remaining size: {current_size / (1024 * 1024):.2f} MB")
        
        logging.info(f"Directory size reduced to {current_size / (1024 * 1024):.2f} MB.")


if __name__ == "__main__":
    secondaryFolder = FolderCleanup(RUMBAFOLDER)

    while True:
        try:
            directorysizeMB = round(secondaryFolder.get_dir_size() / (1024 * 1024), 2)
            logging.info(f"FOLDER: {RUMBAFOLDER} SIZE: {directorysizeMB} MB")
            if directorysizeMB > MAXFOLDERSIZE:
                logging.info(f"Running Cleanup on {RUMBAFOLDER}")
                secondaryFolder.remove_files_until_size(TARGETFOLDERSIZE)  # Reduce to TARGETFOLDERSIZE
            time.sleep(30)  # Wait for 5 seconds before running again
        except KeyboardInterrupt:
            logging.info("\nMonitoring stopped.")
            break  # Exit the loop on Ctrl+C

    #print(secondaryFolder.get_size(RUMBAFOLDER), 'bytes')