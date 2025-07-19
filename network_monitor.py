#!/usr/bin/env python3
import argparse
import time
import sys
import psutil
from typing import Optional
from datetime import datetime

def get_network_stats(interface: Optional[str] = None) -> dict:
    """Retrieve network statistics for the specified interface or all interfaces."""
    try:
        net_io = psutil.net_io_counters(pernic=True)
        if interface and interface not in net_io:
            raise ValueError(f"Interface '{interface}' not found. Available: {list(net_io.keys())}")
        
        stats = {}
        if interface:
            stats[interface] = net_io[interface]
        else:
            stats = net_io
        return stats
    except Exception as e:
        print(f"Error retrieving network stats: {str(e)}", file=sys.stderr)
        return {}

def format_bytes(bytes_count: int) -> str:
    """Convert bytes to human-readable format (e.g., KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.2f} PB"

def print_network_stats(stats: dict, timestamp: str) -> None:
    """Print network statistics to the terminal."""
    if not stats:
        print(f"[{timestamp}] Error: No network data available.")
        return

    print(f"[{timestamp}] Network Statistics:")
    for iface, data in stats.items():
        print(f"  Interface: {iface}")
        print(f"    Bytes Sent: {format_bytes(data.bytes_sent)}")
        print(f"    Bytes Received: {format_bytes(data.bytes_recv)}")
        print(f"    Packets Sent: {data.packets_sent}")
        print(f"    Packets Received: {data.packets_recv}")
        print(f"    Errors In: {data.errin}")
        print(f"    Errors Out: {data.errout}")
        print(f"    Dropped In: {data.dropin}")
        print(f"    Dropped Out: {data.dropout}")
    print("-" * 50)

def main():
    """Main function to parse arguments and monitor network activity."""
    parser = argparse.ArgumentParser(
        description="CLI-based network monitor for Raspberry Pi."
    )
    parser.add_argument(
        "--interface",
        type=str,
        help="Network interface to monitor (e.g., eth0, wlan0; default: all interfaces)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Interval between updates in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        help="Duration to monitor in seconds (default: run until stopped)"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.interval <= 0:
        print("Error: Interval must be a positive number.", file=sys.stderr)
        sys.exit(1)
    if args.duration is not None and args.duration <= 0:
        print("Error: Duration must be a positive number.", file=sys.stderr)
        sys.exit(1)

    # Monitor network
    start_time = time.time()
    try:
        while True:
            if args.duration and (time.time() - start_time) > args.duration:
                print("Monitoring duration reached. Stopping.")
                break

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stats = get_network_stats(args.interface)
            print_network_stats(stats, timestamp)
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
