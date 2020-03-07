from multiprocessing import Process
import os
import ntpath
import subprocess
import time

TEXT_FILE_LOCATION = "/Users/jeetkhondker/Projects/util-projects/sample.txt"
BATCH_FILE_LOCATION = "/Users/jeetkhondker/Projects/util-projects/batch_file_execution.bat"

# Reading File From Client/User Side
# Taking User Request
def read_file():
    global file_location, file_extension, file_name, contents

    # Extracting File Name & File Extension From File Path
    file_location, file_extension = os.path.splitext(TEXT_FILE_LOCATION)

    file_name = ntpath.basename(file_location)
    print("File: ", file_name)
    print("File Extension: ", file_extension)

    # Opening & Reading File
    file = open(TEXT_FILE_LOCATION, 'r')
    contents = ''

    for content in file:
        contents = contents + content

    print("File Contents: ", contents)

# Task Registration
# Mocking of Inserting Into Task Table
def task_register():
    task_table = {"Parent Task ID": os.getpid(), "Parent Task Name": __name__, "File Location": TEXT_FILE_LOCATION, "Contents": contents}
    task_event_table = {"Parent Task ID": os.getpid()}

    print("Task Table: ", task_table)
    print("Task Event Table: ", task_event_table)

# Task Monitor
def task_monitor(title):
    print(title)
    print("Module Name: ", __name__)
    print("Task ID: ", os.getpid())

    read_file()

    task_register()

# Function: Batch File Execution
def batch_file_exec(name):
    print("Parent Task ID: ", os.getppid())
    print("Child Task Name: ", name)
    print("Child Task ID: ", os.getpid())
    print("Starting Batch File Execution . . .")

    subprocess.Popen(BATCH_FILE_LOCATION, shell = True)

# Function: Open Text File
def open_text_file(name):
    print("Parent Task ID: ", os.getppid())
    print("Child Task Name: ", name)
    print("Child Task ID: ", os.getpid())
    print("Opening Text File . . .")

    subprocess.Popen(TEXT_FILE_LOCATION, shell = True)

# Main Program
if __name__ == "__main__":
    task_monitor("Task Registration Monitor")

    # Child Task 1: Batch File Execution
    batch_exec = Process(target = batch_file_exec, args = ("Batch File Execution", ))
    batch_exec.start()
    batch_exec.join()

    # Child Task 2: Open Text File
    open_txt_file = Process(target = open_text_file, args = ("Open Text File", ))
    open_txt_file.start()
    open_txt_file.join()

    # Pausing 3 seconds
    time.sleep(3)

    print("Creation of child tasks from parent task successfully completed!")













