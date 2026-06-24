import pandas as pd
import matplotlib.pyplot as plt

def generate_performance_trends():
    # 24-hour resource monitoring metrics
    metrics_timeline = {
        "Hour": list(range(1, 11)),
        "MemoryUsage_GB": [4.1, 4.2, 4.5, 5.8, 7.2, 7.5, 5.1, 4.6, 4.3, 4.1],
        "CPU_Load_Pct": [12, 15, 22, 65, 88, 92, 40, 20, 14, 11]
    }

    df = pd.DataFrame(metrics_timeline)

    # Create double-axes tracking canvas
    fig, ax1 = plt.subplots(figsize=(8, 4.5))

    # Plot Line A: Memory allocation metrics (Left Axis)
    color = '#3498db'
    ax1.set_xlabel('Operation Hour Timeline')
    ax1.set_ylabel('Memory Allotted (GB)', color=color)
    ax1.plot(df['Hour'], df['MemoryUsage_GB'], color=color, linewidth=2.5, marker='o', label='RAM Allocation')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # instantiate a second axes that shares the same x-axis
    ax2 = ax1.twinx()  
    color = '#e74c3c'
    ax2.set_ylabel('CPU Utilization %', color=color)
    ax2.plot(df['Hour'], df['CPU_Load_Pct'], color=color, linewidth=2, linestyle='--', marker='s', label='CPU Burden')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Infrastructure Hardware Resource Diagnostics Profile')
    fig.tight_layout()
    
    # Render and dump chart file directly to host machine disc storage
    plt.savefig("system_telemetry_profile.png", dpi=300)
    plt.close()
    print(" High-definition visualization compiled and written to: 'system_telemetry_profile.png'")

if __name__ == "__main__":
    generate_performance_trends()
