import os
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification  # <--- Switched to plyer

# --- CONFIGURATION ---
# TRACK_PATH = input("Enter the directory to monitor (e.g., C:\\Users\\YourName\\Downloads): ").strip()
TRACK_PATH = os.path.expanduser("~/Downloads")  # Default to user's Downloads folder

if not os.path.isdir(TRACK_PATH):
    print("Invalid directory. Please check the path and try again.")
    while True:        
        TRACK_PATH = input("Enter the directory to monitor (e.g., C:\\Users\\YourName\\Downloads): ").strip()
        if os.path.isdir(TRACK_PATH):
            break


LOG_FILE = os.path.join(TRACK_PATH, "organizer_log.txt")

# Destination Folders
DEST_DIR_PDF = os.path.join(TRACK_PATH, "All_PDFs")
DEST_DIR_IMAGES = os.path.join(TRACK_PATH, "All_Images")
DEST_DIR_VIDEO = os.path.join(TRACK_PATH, "All_Videos")
DEST_DIR_DOCS = os.path.join(TRACK_PATH, "All_Documents")
DEST_DIR_ARCHIVE = os.path.join(TRACK_PATH, "All_Archives")
DEST_DIR_EXEC = os.path.join(TRACK_PATH, "All_Executables")
DEST_DIR_WEB = os.path.join(TRACK_PATH, "All_Web_Pages")
DEST_DIR_OTHER = os.path.join(TRACK_PATH, "All_Other_Files")

EXTENSION_MAP = {
    ".pdf": DEST_DIR_PDF,
    ".docx": DEST_DIR_DOCS, ".doc": DEST_DIR_DOCS, ".txt": DEST_DIR_DOCS,
    ".jpg": DEST_DIR_IMAGES, ".jpeg": DEST_DIR_IMAGES, ".png": DEST_DIR_IMAGES, ".gif": DEST_DIR_IMAGES,
    ".mp4": DEST_DIR_VIDEO, ".mkv": DEST_DIR_VIDEO, ".mov": DEST_DIR_VIDEO,
    ".zip": DEST_DIR_ARCHIVE, ".rar": DEST_DIR_ARCHIVE, ".7z": DEST_DIR_ARCHIVE, ".torrent": DEST_DIR_ARCHIVE,
    ".exe": DEST_DIR_EXEC, ".msi": DEST_DIR_EXEC,
    ".html": DEST_DIR_WEB, ".htm": DEST_DIR_WEB,
}

logging.basicConfig(
    filename=LOG_FILE, 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def move_file(file_path, notify=False):
    if not os.path.exists(file_path):
        return

    filename = os.path.basename(file_path)
    
    protected_names = [os.path.basename(d) for d in [
        DEST_DIR_PDF, DEST_DIR_IMAGES, DEST_DIR_VIDEO, 
        DEST_DIR_DOCS, DEST_DIR_ARCHIVE, DEST_DIR_EXEC, 
        DEST_DIR_WEB, DEST_DIR_OTHER
    ]]
    
    if filename in ["fileorganizer.py", "organizer_log.txt"] or filename in protected_names:
        return

    file_extension = os.path.splitext(file_path)[1].lower()
    dest_folder = EXTENSION_MAP.get(file_extension, DEST_DIR_OTHER)
    
    os.makedirs(dest_folder, exist_ok=True)
    new_path = os.path.join(dest_folder, filename)

    if os.path.exists(new_path):
        name, ext = os.path.splitext(filename)
        new_path = os.path.join(dest_folder, f"{name}_{int(time.time())}{ext}")

    try:
        shutil.move(file_path, new_path)
        msg = f"SUCCESS: Moved {filename} to {os.path.basename(dest_folder)}"
        print(msg)
        logging.info(msg)

        if notify:
            notification.notify(
                title="File Organized",
                message=f"{filename} moved to {os.path.basename(dest_folder)}",
                app_name="Python Organizer",
                timeout=3
            )

    except PermissionError:
        logging.warning(f"WAITING: {filename} is in use.")
    except Exception as e:
        logging.error(f"ERROR: {e}")

def sweep_existing_files():
    print("--- Initial Sweep Starting ---")
    time.sleep(10)  # Wait for any ongoing downloads to finish
    for filename in os.listdir(TRACK_PATH):
        full_path = os.path.join(TRACK_PATH, filename)
        if os.path.isfile(full_path):
            move_file(full_path, notify=False)
    print("--- Initial Sweep Complete ---\n")

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(2) 
            move_file(event.src_path, notify=True)

if __name__ == "__main__":
    sweep_existing_files()
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, TRACK_PATH, recursive=False)
    
    print(f"Monitoring: {TRACK_PATH}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()