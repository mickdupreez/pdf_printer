import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class on_created(FileSystemEventHandler):
    def __init__(self, printer_name, keywords):
        self.printer_name = printer_name
        self.keywords = keywords

    def on_created(self, event):
        """
        Handles file creation events in the monitored directory.

        Parameters:
        event (FileSystemEvent): an object containing information about the event that occurred.
            For file creation events, this includes the path of the created file (event.src_path).

        If the created file's name contains any of the keywords, it is printed and deleted.
        If an error occurs while printing or deleting the file, it is logged and the process continues.
        """
        # Try to process the file
        try:
            # Check if the filename contains any of the keywords
            if any(keyword in event.src_path for keyword in self.keywords):
                # Try to print the file
                try:
                    print_result = subprocess.run(['lp', '-d', self.printer_name, event.src_path])
                    if print_result.returncode == 0:
                        # If the file was printed successfully, try to delete it
                        try:
                            os.remove(event.src_path)
                            print(f'successfully Printed {event.src_path}')
                            print(f'successfully Deleted {event.src_path}')
                        except OSError as e:
                            # Handle error when deleting file
                            print(f'Error: could not delete {event.src_path} - {e}')
                    else:
                        print(f'Error: could not print {event.src_path}')
                except Exception as e:
                    # Handle error when printing file
                    print(f'Error: {e}')
        except Exception as e:
            print(f'Error: {e}')

            
def print_files(watched_dir, printer_name, keywords):
    """
    Set up the file system observer and start the event loop that listens for file creation events in the specified directory.

    Parameters:
    watched_dir (str): the path of the directory to be monitored.
    printer_name (str): the name of the printer to be used for printing.
    keywords (list): a list of strings representing keywords to be used to identify files to be printed.

    Returns:
    None
    """
    # Check if the watched directory exists and if the script has permission to access it
    if not os.path.exists(watched_dir):
        print(f'Error: the specified directory {watched_dir} does not exist')
        return
    if not os.access(watched_dir, os.R_OK):
        print(f'Error: the program does not have permission to access {watched_dir}')
        return
    
    # Check if the specified printer is available
    printer_status = subprocess.run(['lpstat', '-p', printer_name], capture_output=True)
    if printer_status.returncode != 0:
        print(f'Error: printer {printer_name} is not available')
        return

    # Set up the file system observer and start the event loop
    try:
        # Create an event handler instance with the printer name and keywords as arguments
        event_handler = on_created(printer_name, keywords)
        # Create an Observer instance
        observer = Observer()
        # Schedule the event handler to be called for file creation events in the watched directory
        observer.schedule(event_handler, watched_dir, recursive=False)
        # Start the observer
        observer.start()
    except Exception as e:
        print(f'Error: {e}')
        
    # Run the event loop indefinitely until interrupted by the user
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when the user interrupts the event loop
        observer.stop()
    # Join the observer thread
    observer.join()

# Set the path of the watched directory to the user's Downloads directory
watched_dir = os.path.expanduser('~/Downloads')
# Set the name of the printer to be used
printer_name = 'HP_LaserJet_M402dw__031836_'
# Set the list of keywords to be used to identify files to be printed
keywords = ['WorkConfirmation', 'label_', '_shipper', 'PackingList']
# Call the print_files function with the specified arguments
print_files(watched_dir, printer_name, keywords)