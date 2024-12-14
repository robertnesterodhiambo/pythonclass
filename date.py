
import os
from tabulate import tabulate
import h5py
import platform
import time

def modify_file_dates(file_path, creation_time=None, modification_time=None):
    """
    Modify the creation and modification dates of a file.
    Works across Windows, Linux, and macOS.
    
    Parameters:
        file_path (str): The file path.
        creation_time (float): Epoch timestamp for the creation time.
        modification_time (float): Epoch timestamp for the modification time.
    """
    if modification_time:
        os.utime(file_path, (modification_time, modification_time))

    if creation_time and platform.system() == "Windows":
        import pywintypes
        import win32file
        import win32con

        file_handle = win32file.CreateFile(
            file_path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )

        win_time = pywintypes.Time(creation_time)
        win32file.SetFileTime(file_handle, win_time, None, None)
        file_handle.close()

# Directory containing the models
# Use current directory since models and code are in the same folder
directory = '.'

# List all files in the directory
files = os.listdir(directory)

# Filter the files to include only the `.h5` model files
model_files = [file for file in files if file.endswith('.h5')]

# Prepare data for the table
data = []
for model in model_files:
    # Extract model name by removing the file extension
    model_name = model.replace('lstm_model_', '').replace('.h5', '')
    
    # Gather additional details from the .h5 file
    model_path = os.path.join(directory, model)
    try:
        with h5py.File(model_path, 'r') as h5file:
            # Example details: list datasets or attributes
            datasets = list(h5file.keys())
            details = ', '.join(datasets) if datasets else "No datasets"
    except Exception as e:
        details = f"Error reading: {e}"

    # Optionally modify file dates (example: set to Jan 1, 2022)
    new_time = time.mktime(time.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S"))
    modify_file_dates(model_path, creation_time=new_time, modification_time=new_time)

    data.append([model_name, model, details])

# Define table headers
headers = ["Model Name", "File Name", "Details"]

# Display the table
print(tabulate(data, headers=headers, tablefmt="grid"))
