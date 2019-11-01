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

# Memory Information
print("=" * 40, "Memory Information", "=" * 40)

# Getting The Memory Details
vir_memory = psutil.virtual_memory()
print(f"Total: {get_size(vir_memory.total)}")
print(f"Available: {get_size(vir_memory.available)}")
print(f"Used: {get_size(vir_memory.used)}")
print(f"Percentage: {vir_memory.percent}%")

# Disk Information
print("=" * 40, "Disk Information", "=" * 40)
print("Partitions & Usages: ")

# Getting All Disk Partitions
partitions = psutil.disk_partitions()

for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File System Type: {partition.fstype}")

    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # This Can Be Catched Due To The Disk That Isn't Ready
        continue

    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")

# Getting IO Statistics Since Boot
disk_io = psutil.disk_io_counters()

print(f"Total Bytes Read: {get_size(disk_io.read_bytes)}")
print(f"Total Bytes Written: {get_size(disk_io.write_bytes)}")

# Network Information
print("=" * 40, "Network Information", "=" * 40)

# Getting All Network Interfaces (Virtual & Physical)
interface_address = psutil.net_if_addrs()

for interface_name, interface_addresses in interface_address.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == "AddressFamily.AF_INET":
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == "AddressFamily.AF_PACKET":
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")

# Getting IO Statistics Since Boot
net_io = psutil.net_io_counters()

print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")