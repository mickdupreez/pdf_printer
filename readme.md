## Auto PDF Printer

This script monitors a specified directory for new files and prints them if their names contain any of the specified keywords.

  

## Installation

To use this script, you need to have Python 3 and the pyinotify library installed on your system. You also need access to a printer. You can install the `pyinotify` library using pip, the Python package manager:

    pip install pyinotify

  

## Usage

To use the script, you can run it from the command line by typing python3 print_files_with_keywords.py.

  

By default, the script monitors the ~/Downloads directory and looks for files whose names contain any of the following keywords: WorkConfirmation, label_, _shipper, and PackingList. It prints the files using the printer HP_LaserJet_M402dw__031836_. You can customize these default values by passing arguments to the print_files_with_keywords function:

  
  

    print_files_with_keywords(
    
    downloads_dir='~/Downloads',
    
    printer_name='HP_LaserJet_M402dw__031836_',
    
    keywords=['WorkConfirmation', 'label_', '_shipper', 'PackingList']
    
    )

  

> For example, to change the printer name to My_Printer and the list of
> keywords to ['invoice', 'receipt'], you can call the function like
> this:

  
  

    print_files_with_keywords(
    
    printer_name='My_Printer',
    
    keywords=['invoice', 'receipt']
    
    )

  

## Output

If the specified directory does not exist or the program does not have permission to access it, the script returns an error message. If the specified printer is not available, the script returns an error message. If there was an error while printing a file, the script returns an error message. If the file was successfully printed, the script prints a message indicating that the file was printed and deleted, and then deletes the file. If the file was already deleted, the script prints an error message indicating that the file has already been deleted.

  

## Notes

 - Make sure to replace spaces in the printer name with underscores.
 - The script only looks for files that are created and closed in the
   monitored directory, so it will not pick up files that are already
   present when the script is started.
 - The script only looks for files whose names contain the specified
   keywords, so it will not pick up files whose contents contain the
   keywords.
 - The script only looks for files with the .txt extension, so it will
   not pick up files with other extensions, even if their names contain
   the keywords.
