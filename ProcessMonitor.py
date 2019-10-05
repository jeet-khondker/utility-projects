# Importing Libraries
import psutil
from datetime import datetime
import pandas as pd

# Function: Printing Bytes (Display Manipulation)
# Returns Size Of Bytes In A Nice Format
def get_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            
            # Returning A Value Having 2 Decimal Places Floating Foint Number
            return f"{bytes:.2f}{unit}B"

        # bytes = bytes / 1024
        bytes /= 1024

# List Containing All Process Dictionaries
processes = []

"""
Retrieving All Processes In A For Loop.
psutil.process_iter(): Returns A Generator Yielding A Process Instance For All Running Processes In The OS
"""

# Iterating Over The Generator
for process in psutil.process_iter():

    # Getting All Process Information In One Shot
    with process.oneshot():

        # Getting The Process ID
        pid = process.pid

        # Getting The Name Of The File Executed
        name = process.name()

        # Getting The Time The Process Was Spawned
        create_time = datetime.fromtimestamp(process.create_time())

        # process.cpu_affinity() Warpped In A try/except Block
        # Reason: Sometimes It Will Raise A psutil.AccessDenied For System Processes
        
        try:

            # Getting The Number Of CPU Cores That Can Execute This Process
            cores = len(process.cpu_affinity())

        except psutil.AccessDenied:
            cores = 0
        
        # Getting The CPU Usage Percentage
        cpu_usage = process.cpu_percent()

        # Getting The Status Of The Process (Running, Idle, etc.)
        status = process.status()

        try:
            
            # Getting The Process Priority (A Lower Value Means A More Prioritized Process)
            process_priority = int(process.nice())
            
        except psutil.AccessDenied:
            process_priority = 0

        try:

            # Getting The Memory Usage Of This Process In Bytes
            memory_usage = process.memory_full_info().uss

        except psutil.AccessDenied:
            memory_usage = 0

        # Total Written & Read Bytes By This Process
        io_counters = process.io_counters()
        read_bytes = io_counters.read_bytes
        write_bytes = io_counters.write_bytes

        # Getting The Number Of Total Threads Spawned By This Process
        total_threads = process.num_threads()

        # Getting The Username Of User Who Spawned The Process
        try:
            username = process.username()
        except psutil.AccessDenied:
            username = "N/A"

        # Adding All Information To Processes List
        processes.append({
            "pid": pid,
            "name": name,
            "create_time": create_time,
            "Cores": cores,
            "cpu_usage": cpu_usage,
            "status": status,
            "process_priority": process_priority,
            "memory_usage": memory_usage,
            "read_bytes": read_bytes,
            "write_bytes": write_bytes,
            "total_threads": total_threads,
            "username": username,
            })

        # Converting To Pandas Dataframe
        data_frame = pd.DataFrame(processes)

        # Setting The Process ID As Index Of A Process
        data_frame.set_index("pid", inplace = True)

        # Command Line Argument Parsing
        # Main Program
        if __name__ == "__main__":

            # Import argparse Module: For User-Friendly Command Line Interfaces
            import argparse

            # Setting Up A Desctiprion For The Argument Parser
            parser = argparse.ArgumentParser(description = "Process Viewer & Monitor")

            # Adding Arguments
            parser.add_argument("-c", "--columns", help = """Columns To Show,
                                                Available: name, create_time, cpu_usage, status, process_priority, memory_usage, read_bytes, write_bytes, total_threads, username.
                                                Default: name, cpu_usage, memory_usage, read_bytes, write_bytes, status, create_time, process_priority, total_threads, cores.""",
                                default = "name, cpu_usage, memory_usage, read_bytes, write_bytes, status, create_time, process_priority, total_threads, cores")
            parser.add_argument("-s", "--sort-by", dest = "sort_by", help = "Column To Sort By, Default: memory_usage .", default = "memory_usage")
            parser.add_argument("--descending", action = "store_true", help = "Whether To Sort In Descending Order.")
            parser.add_argument("-n", help = "Number Of Processes To Show, It Will Show All If 0 Is Specified. Default: 25 .", default = 25)

            # Parse Arguments
            args = parser.parse_args()
            columns = args.columns
            sort_by = args.sort_by
            descending = args.descending
            n = int(args.n)

            # Sorting Rows By The Column Passed As Argument
            data_frame.sort_values(sort_by, inplace = True, ascending = not descending)

            # Pretty Printing Bytes
            data_frame["memory_usage"] = data_frame["memory_usage"].apply(get_size)
            data_frame["write_bytes"] = data_frame["write_bytes"].apply(get_size)
            data_frame["read_bytes"] = data_frame["read_bytes"].apply(get_size)

            # Converting To Proper Date Format
            data_frame["create_time"] = data_frame["create_time"].apply(datetime.strftime, arges = ("%Y-%m-%d %H:%M:%S",))

            # Defining What Columns To Show Based On What Is Passed In The Arguments
            data_frame = data_frame[columns.split(',')]

            # Number Of Processes To Show
            # It Will Show All If 0 Is Specified, Default Is 25
            if n == 0:
                print(data_frame.to_string())
            elif n > 0:
                print(data_frame.head(n).to_string())