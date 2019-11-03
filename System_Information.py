import psutil
import platform # Used To Access The Underlying Platform's Data such as H/W, OS & Interpreter Version Information
from datetime import datetime, date

# Importing SMTP & Email Libraries
import smtplib
from email.mime.text import MIMEText

# Importing Twilio For Sending SMS Notifications
from twilio.rest import Client

# Importing Credentials File
import credentials

# Getting Today Information
today = date.today()

message_subject = "Current System Information Update - " + today.strftime("%d/%m/%Y")
message = ""

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
message += "=" * 40 + "SYSTEM INFORMATION" + "=" * 40 + "\n"
# print("=" * 40, "System Information", "=" * 40)
username = platform.uname()
message += "System: " + username.system + "\n"
# print(f"System: {username.system}")
message += "Node Name: " + username.node + "\n"
# print(f"Node Name: {username.node}")
message += "Release: " + username.release + "\n"
# print(f"Release: {username.release}")
message += "Version: " + username.version + "\n"
# print(f"Version: {username.version}")
message += "Machine: " + username.machine + "\n"
# print(f"Machine: {username.machine}")
message += "Processor: " + username.processor + "\n"
# print(f"Processor: {username.processor}")

# Boot Time
message += "=" * 40 + "BOOT TIME" + "=" * 40 + "\n"
# print("=" * 40, "Boot Time", "=" * 40)
boot_time_timestamp = psutil.boot_time()
boot_time = datetime.fromtimestamp(boot_time_timestamp)
message += "Boot Time: " + str(boot_time.year) + "/" + str(boot_time.month) + "/" + str(boot_time.day) + " " + str(boot_time.hour) + ":" + str(boot_time.minute) + ":" + str(boot_time.second) + "\n"
# print(f"Boot Time: {boot_time.year}/{boot_time.month}/{boot_time.day} {boot_time.hour}:{boot_time.minute}:{boot_time.second}")

# CPU Information
message += "=" * 40 + "CPU INFORMATION" + "=" * 40 + "\n"
# print("=" * 40, "CPU Information", "=" * 40)

# Number Of Cores
message += "Physical Cores: " + str(psutil.cpu_count(logical = False)) + "\n"
# print("Physical Cores: ", psutil.cpu_count(logical = False))
message += "Total Cores: " + str(psutil.cpu_count(logical = True)) + "\n"
# print("Total Cores: ", psutil.cpu_count(logical = True))

# CPU Frequencies
cpu_frequency = psutil.cpu_freq()
message += "Maximum Frequency: " + str(float("{0:.2f}".format(cpu_frequency.max))) + "MHz" + "\n"
# print(f"Maximum Frequency: {cpu_frequency.max: .2f}MHz")
message += "Minimum Frequency: " + str(float("{0:.2f}".format(cpu_frequency.min))) + "MHz" + "\n"
# print(f"Minimum Frequency: {cpu_frequency.min: .2f}MHz")
message += "Current Frequency: " + str(float("{0:.2f}".format(cpu_frequency.current))) + "MHz" + "\n"
# print(f"Current Frequency: {cpu_frequency.current: .2f}MHz")

# CPU Usage
for core_number, percentage in enumerate(psutil.cpu_percent(percpu = True)):
    message += "Core " + str(core_number) + ":" + str(percentage) + "%" + "\n"
    # print(f"Core {core_number}: {percentage}%")
message += "Total CPU Usage: " + str(psutil.cpu_percent()) + "%" + "\n"
# print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
message += "=" * 40 + "MEMORY INFORMATION" + "=" * 40 + "\n"
# print("=" * 40, "Memory Information", "=" * 40)

# Getting The Memory Details
vir_memory = psutil.virtual_memory()
message += "Total: " + get_size(vir_memory.total) + "\n"
# print(f"Total: {get_size(vir_memory.total)}")
message += "Available: " + get_size(vir_memory.available) + "\n"
# print(f"Available: {get_size(vir_memory.available)}")
message += "Used: " + get_size(vir_memory.used) + "\n"
# print(f"Used: {get_size(vir_memory.used)}")
message += "Percentage: " + str(vir_memory.percent) + "%" + "\n"
# print(f"Percentage: {vir_memory.percent}%")

# Disk Information
message += "=" * 40 + "DISK INFORMATION" + "=" * 40 + "\n"
# print("=" * 40, "Disk Information", "=" * 40)
message += "PARTITIONS & USAGES: " + "\n"
# print("Partitions & Usages: ")

# Getting All Disk Partitions
partitions = psutil.disk_partitions()

for partition in partitions:
    message += "=== Device: " + partition.device + "===\n"
    # print(f"=== Device: {partition.device} ===")
    message += "  Mountpoint: " + partition.mountpoint + "\n"
    # print(f"  Mountpoint: {partition.mountpoint}")
    message += "  File System Type: " + partition.fstype + "\n"
    # print(f"  File System Type: {partition.fstype}")

    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # This Can Be Catched Due To The Disk That Isn't Ready
        continue

    message += "  Total Size: " + get_size(partition_usage.total) + "\n"
    # print(f"  Total Size: {get_size(partition_usage.total)}")
    message += "  Used: " + get_size(partition_usage.used) + "\n"
    # print(f"  Used: {get_size(partition_usage.used)}")
    message += "  Free: " + get_size(partition_usage.free) + "\n"
    # print(f"  Free: {get_size(partition_usage.free)}")
    message += "  Percentage: " + str(partition_usage.percent) + "%" + "\n"
    # print(f"  Percentage: {partition_usage.percent}%")

# Getting IO Statistics Since Boot
disk_io = psutil.disk_io_counters()

message += "Total Bytes Read: " + get_size(disk_io.read_bytes) + "\n"
# print(f"Total Bytes Read: {get_size(disk_io.read_bytes)}")
message += "Total Bytes Written: " + get_size(disk_io.write_bytes) + "\n"
# print(f"Total Bytes Written: {get_size(disk_io.write_bytes)}")

# Network Information
message += "=" * 40 + "NETWORK INFORMATION" + "=" * 40 + "\n"
# print("=" * 40, "Network Information", "=" * 40)

# Getting All Network Interfaces (Virtual & Physical)
interface_address = psutil.net_if_addrs()

for interface_name, interface_addresses in interface_address.items():
    for address in interface_addresses:
        message += "=== Interface: " + interface_name + "===\n"
        # print(f"=== Interface: {interface_name} ===")
        if str(address.family) == "AddressFamily.AF_INET":
            message += "  IP Address: " + address.address + "\n"
            # print(f"  IP Address: {address.address}")
            message += "  Netmask: " + address.netmask + "\n"
            # print(f"  Netmask: {address.netmask}")
            message += "  Broadcast IP: " + str(address.broadcast) + "\n"
            # print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == "AddressFamily.AF_PACKET":
            message += "  MAC Address: " + address.address + "\n"
            # print(f"  MAC Address: {address.address}")
            message += "  Netmask: " + address.netmask + "\n"
            # print(f"  Netmask: {address.netmask}")
            message += "  Broadcast MAC: " + address.broadcast + "\n"
            # print(f"  Broadcast MAC: {address.broadcast}")

# Getting IO Statistics Since Boot
net_io = psutil.net_io_counters()

message += "Total Bytes Sent: " + get_size(net_io.bytes_sent) + "\n"
# print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
message += "Total Bytes Received: " + get_size(net_io.bytes_recv) + "\n"
# print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

# Making The Message To MIMEText
msg = MIMEText(message)

# Taking The Subject
msg["Subject"] = message_subject

# Taking The Sender Email Address
msg["From"] = credentials.sender

# Taking The Receiver's Email From The Receipient List
msg["To"] = credentials.receiver

try:
    # Using The Google SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # Identifying To An ESMTP Server
    server.ehlo()

    # Starting The TLS
    server.starttls()

    # Identifying To An ESMTP Server
    server.ehlo()

    # Login With Email Adddress & Password
    server.login(credentials.sender, credentials.password)

    # Sending Email
    server.sendmail(credentials.sender, credentials.receiver, msg.as_string())

    # Closing The Server Connection
    server.close()

    # Twillio SMS Notification
    client = Client(credentials.accountSID, credentials.authToken)
    sms = client.messages.create(body = "Current System Information Email Sent Successfully!", from_ = credentials.from_number, to = credentials.to_number)
    # print("Email Sent Successfully!")

except smtplib.SMTPException:
    # Twillio SMS Notification
    client = Client(credentials.accountSID, credentials.authToken)
    sms = client.messages.create(body = "ERROR: Unable To Send Current System Information Email!", from_ = credentials.from_number, to = credentials.to_number)
    # print("ERROR: Unable To Send Email!")