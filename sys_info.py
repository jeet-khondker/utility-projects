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

print("=" * 40, "System Information", "=" * 40)
username = platform.uname()
print(f"System: {username.system}")
print(f"Node Name: {username.node}")
print(f"Release: {username.release}")
print(f"Version: {username.version}")
print(f"Machine: {username.machine}")
print(f"Processor: {username.processor}")




