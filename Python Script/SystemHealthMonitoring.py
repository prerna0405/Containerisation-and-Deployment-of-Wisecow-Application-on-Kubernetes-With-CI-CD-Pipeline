""" System Health Monitoring Script :- 
Problem Statement - 
    Develop a script that monitors the health of a Linux system. It should check
    CPU usage, memory usage, disk space, and running processes. If any of
    these metrics exceed predefined thresholds (e.g., CPU usage > 80%), the
    script should send an alert to the console or a log file.
"""

import os
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='system_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define thresholds
CPU_THRESHOLD = 80.0  # percentage
MEMORY_THRESHOLD = 80.0  # percentage
DISK_THRESHOLD = 80.0  # percentage
PROCESS_THRESHOLD = 300  # number of processes

def get_cpu_usage():
    with open('/proc/stat', 'r') as file:
        line = file.readline()
        cpu_times = list(map(int, line.split()[1:]))
        idle_time = cpu_times[3]
        total_time = sum(cpu_times)
    return idle_time, total_time

def calculate_cpu_usage(idle_time_1, total_time_1, idle_time_2, total_time_2):
    idle_delta = idle_time_2 - idle_time_1
    total_delta = total_time_2 - total_time_1
    cpu_usage = 100.0 * (1.0 - idle_delta / total_delta)
    return cpu_usage

def check_cpu_usage():
    idle_time_1, total_time_1 = get_cpu_usage()
    time.sleep(1)
    idle_time_2, total_time_2 = get_cpu_usage()
    cpu_usage = calculate_cpu_usage(idle_time_1, total_time_1, idle_time_2, total_time_2)
    if cpu_usage > CPU_THRESHOLD:
        alert_message = f"High CPU usage detected: {cpu_usage:.2f}%"
        alert(alert_message)
    return cpu_usage

def check_memory_usage():
    with open('/proc/meminfo', 'r') as file:
        lines = file.readlines()
    mem_total = int(lines[0].split()[1])
    mem_available = int(lines[2].split()[1])
    memory_usage = 100.0 * (1 - mem_available / mem_total)
    if memory_usage > MEMORY_THRESHOLD:
        alert_message = f"High memory usage detected: {memory_usage:.2f}%"
        alert(alert_message)
    return memory_usage

def check_disk_usage():
    statvfs = os.statvfs('/')
    total_blocks = statvfs.f_blocks
    free_blocks = statvfs.f_bfree
    disk_usage = 100.0 * (1 - free_blocks / total_blocks)
    if disk_usage > DISK_THRESHOLD:
        alert_message = f"High disk usage detected: {disk_usage:.2f}%"
        alert(alert_message)
    return disk_usage

def check_running_processes():
    process_count = len([name for name in os.listdir('/proc') if name.isdigit()])
    if process_count > PROCESS_THRESHOLD:
        alert_message = f"High number of running processes detected: {process_count}"
        alert(alert_message)
    return process_count

def alert(message):
    print(message)
    logging.info(message)

def monitor_system():
    while True:
        cpu = check_cpu_usage()
        memory = check_memory_usage()
        disk = check_disk_usage()
        processes = check_running_processes()
        print(f"CPU Usage: {cpu:.2f}% | Memory Usage: {memory:.2f}% | Disk Usage: {disk:.2f}% | Running Processes: {processes}")
        # Sleep for a minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    monitor_system()
