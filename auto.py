import os
import shutil
from os.path import splitext, exists
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

source_dir = r"C:\Users\lenov\Downloads"
images_dir = r"C:\Users\lenov\Downloads\Images"
documents_dir = r"C:\Users\lenov\Downloads\Documents"

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1 #if file name does exist, add number to make it unique

    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1 # move counter since previous number has been used
    
    return name

def moveFile(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(dest, name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)



with os.scandir(source_dir) as entries:
    for entry in entries:
        print(entry.name)

class FileMoverHandler(FileSystemEventHandler):
    def on_change(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_images(entry, name)
                self.check_documents(entry, name)
                
    def check_images(self, entry, name):
        for ext in image_extensions:
            if name.endswith(ext) or name.endswith(ext.upper()):
                moveFile(images_dir, entry, name)
                logging.info(f"Moved image file: {name}")
    def check_documents(self, entry, name):
        for ext in document_extensions:
            if name.endswith(ext) or name.endswith(ext.upper()):
                moveFile(documents_dir, entry, name)
                logging.info(f"Moved document file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileMoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

