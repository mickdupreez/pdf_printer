import os
import subprocess
import time
import pyinotify

def print_files_with_keywords(downloads_dir='~/Downloads', printer_name='HP_LaserJet_M402dw__031836_', keywords=['WorkConfirmation', 'label_', '_shipper', 'PackingList']):
    """
    Monitors a specified directory for new files and prints them if their names contain any of the specified keywords.

    Parameters:
    - downloads_dir (str): The directory to be monitored for new files. Default is '~/Downloads'.
    - printer_name (str): The name of the printer to use for printing. Default is 'HP_LaserJet_M402dw__031836_'.
    - keywords (list[str]): A list of keywords to search for in the file names. Default is ['WorkConfirmation', 'label_', '_shipper', 'PackingList'].

    Returns:
    - None. If the specified directory does not exist or the program does not have permission to access it, returns an error message. If the specified printer is not available, returns an error message. If there was an error while printing a file, returns an error message.
    """
    # Check if the specified directory exists and if the program has permission to access it
    if not os.path.exists(downloads_dir) or not os.access(downloads_dir, os.R_OK):
        return 'Error: the specified directory does not exist or the program does not have permission to access it'

    # Check if the specified printer is available
    printer_status = subprocess.run(['lpstat', '-p', printer_name], capture_output=True)
    if printer_status.returncode != 0:
        return f'Error: printer {printer_name} is not available'

    # Create a WatchManager and a Notifier to monitor the specified directory for new files
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm)
    wm.add_watch(downloads_dir, pyinotify.IN_CLOSE_WRITE)

    # Define an event handler class that will be called whenever a new file is created and closed in the monitored directory
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            # Get the name of the new file
            file = event.name
            # Check if the file name contains any of the specified keywords
            if any(keyword in file for keyword in keywords):
                # Construct the full path to the file
                file_path = os.path.join(downloads_dir, file)
                # Try to print the file
                print_result = subprocess.run(['lp', '-d', printer_name, file_path])
                # If the file was successfully printed, delete it
                if print_result.returncode == 0:
                    try:
                        os.remove(file_path)
                        print(f'Printed and deleted the file {file}')
                        time.sleep(1)
                    except FileNotFoundError:
                        # If the file was already deleted, print an error message
                        print(f'Error: {file} has already been deleted')
                else:
                    # If there was an error while printing, return an error message
                    return f'Error: could not print {file}'

    # Create an instance of the event handler class
    handler = EventHandler()
    # Start the notifier loop to monitor the directory for new files
    notifier.loop()

print_files_with_keywords()