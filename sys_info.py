import psutil
import platform # Used To Access The Underlying Platform's Data such as H/W, OS & Interpreter Version Information
from datetime import datetime

# Function: Getting The Size
# Converting Large Number Of Bytes Into A Scaled Format (Eg. In Kilo, Mega, Giga Etc.)
def get_size(bytes, suffix = 'B'):
    """
    Scale Bytes To Its Proper Format
    e.g.
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}" # 1.17GB
        bytes /= factor # bytes = bytes / factor

# System Information
print("=" * 40, "System Information", "=" * 40)
username = platform.uname()
print(f"System: {username.system}")
print(f"Node Name: {username.node}")
print(f"Release: {username.release}")
print(f"Version: {username.version}")
print(f"Machine: {username.machine}")
print(f"Processor: {username.processor}")

# Boot Time
print("=" * 40, "Boot Time", "=" * 40)
boot_time_timestamp = psutil.boot_time()
boot_time = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {boot_time.year}/{boot_time.month}/{boot_time.day} {boot_time.hour}:{boot_time.minute}:{boot_time.second}")

# CPU Information
print("=" * 40, "CPU Information", "=" * 40)

# Number Of Cores
print("Physical Cores: ", psutil.cpu_count(logical = False))
print("Total Cores: ", psutil.cpu_count(logical = True))

# CPU Frequencies
cpu_frequency = psutil.cpu_freq()
print(f"Maximum Frequency: {cpu_frequency.max: .2f}MHz")
print(f"Minimum Frequency: {cpu_frequency.min: .2f}MHz")
print(f"Current Frequency: {cpu_frequency.current: .2f}MHz")

# CPU Usage
for core_number, percentage in enumerate(psutil.cpu_percent(percpu = True)):
    print(f"Core {core_number}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")




