#!/usr/bin/env python
import os
import subprocess
import time



def main():
    # The directory where the script will look for files to print
    downloads_dir = os.path.expanduser('~/Downloads')

    # The name of the printer that the script will use
    printer_name = 'HP_LaserJet_M402dw__031836_'

    # A list of keywords that will be used to identify files to print
    keywords = ['WorkConfirmation', 'label_', '_shipper', 'PackingList']

    # Check if the downloads directory exists and if the script has permission to access it
    if not os.path.exists(downloads_dir) or not os.access(downloads_dir, os.R_OK):
        # If the directory does not exist or the script does not have permission to access it, print an error message and exit
        print('Error: the specified directory does not exist or the program does not have permission to access it')
        exit(1)

    # Check if the printer is available
    printer_status = subprocess.run(['lpstat', '-p', printer_name], capture_output=True)
    if printer_status.returncode != 0:
        # If the printer is not available, print an error message and exit
        print(f'Error: printer {printer_name} is not available')
        exit(1)

    # Run the script in an infinite loop
    while True:
        # Get a list of all the files in the Downloads directory
        files = os.listdir(downloads_dir)

        # Iterate over the list of files
        for file in files:
            # Check if any of the keywords are in the file name
            if any(keyword in file for keyword in keywords):
                # Construct the full path to the file
                file_path = os.path.join(downloads_dir, file)

                # Print the file
                print_result = subprocess.run(['lp', '-d', printer_name, file_path])

                # Check if the print command was successful
                if print_result.returncode == 0:
                    # If the print was successful, delete the file
                    os.remove(file_path)
                    print(f'Deleted {file}')
                    # Sleep for 2 seconds before checking for more files
                    time.sleep(2)
                else:
                    # If the print was not successful, print an error message
                    print(f'Error: could not print {file}')

        # Sleep for 3 seconds before checking for new files again
        time.sleep(3)


if __name__ == "__main__":
    main()