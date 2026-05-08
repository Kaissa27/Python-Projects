import psutil
import time
import os

def monitor_system(threshold_cpu=80, threshold_ram=80):
    print("--- SYSTEM HEALTH MONITOR (Press Ctrl+C to stop) ---")
    
    try:
        while True:
            # 1. Gather hardware data
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            
            # 2. Clear the terminal (makes it look like a real app)
            # 'cls' for Windows, 'clear' for Mac/Linux
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(f"CPU Usage: {cpu_usage}%")
            print(f"RAM Usage: {ram_usage}%")
            print("-" * 20)

            # 3. Alert Logic
            if cpu_usage > threshold_cpu:
                print("⚠️ WARNING: High CPU usage detected!")
            if ram_usage > threshold_ram:
                print("⚠️ WARNING: Running low on Memory!")

            # Wait before checking again
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

# monitor_system(threshold_cpu=70, threshold_ram=75)
