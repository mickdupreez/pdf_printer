import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PrintHandler(FileSystemEventHandler):
    def __init__(self, printer_name, keywords):
        """
        Initialize the event handler with the printer name and keywords to match.

        Parameters:
        printer_name (str): The name of the printer to use for printing.
        keywords (list): A list of strings to match against the file names.
        """
        self.printer_name = printer_name
        self.keywords = keywords

    def on_created(self, event):
        """
        This method is called whenever a new file is added to the directory being watched.
        It checks if the file name contains any of the keywords and, if it does, attempts to print and delete the file.

        Parameters:
        event (FileSystemEvent): An event object containing information about the file that was added.
        """
        # Check if the file name contains any of the keywords
        if any(keyword in event.src_path for keyword in self.keywords):
            # Print the file using the lp command
            print_result = subprocess.run(['lp', '-d', self.printer_name, event.src_path])
            if print_result.returncode == 0:
                # The print was successful, so delete the file using the os.remove() function
                os.remove(event.src_path)
                print(f'successfully Printed {event.src_path}')
                print(f'successfully Deleted {event.src_path}')
            else:
                # There was an error printing the file
                print(f'Error: could not print {event.src_path}')

def print_files(downloads_dir, printer_name, keywords):
    """
    Set up a watchdog observer to watch the specified directory for changes, and print and delete
    files with names that contain certain keywords when they are added to the directory.

    Parameters:
    downloads_dir (str): The directory to watch for changes.
    printer_name (str): The name of the printer to use for printing.
    keywords (list): A list of strings to match against the file names.
    """
    # Check if the specified directory exists and is readable
    if not os.path.exists(downloads_dir) or not os.access(downloads_dir, os.R_OK):
        print('Error: the specified directory does not exist or the program does not have permission to access it')
        return
    
    # Check if the specified printer is available
    printer_status = subprocess.run(['lpstat', '-p', printer_name], capture_output=True)
    if printer_status.returncode != 0:
        print(f'Error: printer {printer_name} is not available')
        return

    # Set up the watchdog observer
    event_handler = PrintHandler(printer_name, keywords)
    observer = Observer()
    observer.schedule(event_handler, downloads_dir, recursive=False)
    observer.start()
    try:
        # Run the observer loop indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when the program is interrupted
        observer.stop()
    observer.join()

# Set the directory to watch and the printer to use
downloads_dir = os.path.expanduser('~/Downloads')
printer_name = 'HP_LaserJet_M402dw__031836_'
keywords = ['WorkConfirmation', 'label_', '_shipper', 'PackingList']

# Start watching the directory for changes
print_files(downloads_dir, printer_name, keywords)