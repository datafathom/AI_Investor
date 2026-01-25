
from services.monitoring.health_monitor import get_health_monitor

def run_health_check(args=None):
    """
    Test Phase 31 Health Monitor.
    """
    print("Testing System Health Monitor...")
    
    monitor = get_health_monitor()
    vitals = monitor.get_system_vitals()
    
    print("\n--- SYSTEM VITALS ---")
    print(f"CPU Usage:    {vitals['cpu_percent']}%")
    print(f"Memory Usage: {vitals['memory_percent']}%")
    print(f"Disk Usage:   {vitals['disk_percent']}%")
    print(f"Status:       {vitals['status']}")
    
    if vitals['status'] == "HEALTHY":
        print("OK System is Healthy.")
    else:
        print("WARN System Load High.")
