#!/usr/bin/env python3
import argparse
import time
import datetime
import random
import os
import sys
import logging
from typing import Optional

def setup_logger(log_file: str, log_level: str = "INFO") -> logging.Logger:
    """Set up the logger with specified file and log level."""
    logger = logging.getLogger("SensorLogger")
    logger.setLevel(getattr(logging, log_level.upper()))

    # File handler
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def simulate_sensor_data() -> dict:
    """Simulate sensor data (temperature, humidity, pressure)."""
    return {
        "temperature": round(random.uniform(15.0, 35.0), 2),  # Celsius
        "humidity": round(random.uniform(30.0, 90.0), 2),    # Percentage
        "pressure": round(random.uniform(900.0, 1100.0), 2)  # hPa
    }

def log_sensor_data(logger: logging.Logger, interval: int, duration: Optional[int] = None) -> None:
    """Log sensor data periodically."""
    start_time = time.time()
    try:
        while True:
            # Check if duration is set and exceeded
            if duration and (time.time() - start_time) > duration:
                logger.info("Logging duration reached. Stopping.")
                break

            data = simulate_sensor_data()
            logger.info(
                f"Sensor Data - Temp: {data['temperature']}°C, "
                f"Humidity: {data['humidity']}%, Pressure: {data['pressure']}hPa"
            )
            time.sleep(interval)

    except KeyboardInterrupt:
        logger.info("Logging stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

def validate_args(args: argparse.Namespace) -> None:
    """Validate command-line arguments."""
    if args.interval <= 0:
        raise ValueError("Interval must be a positive number.")
    if args.duration is not None and args.duration <= 0:
        raise ValueError("Duration must be a positive number.")
    if os.path.exists(args.log_file) and not args.append:
        raise FileExistsError(f"Log file '{args.log_file}' already exists. Use --append to append or choose a different file.")

def main():
    """Main function to parse arguments and start logging."""
    parser = argparse.ArgumentParser(
        description="CLI-based file logger for periodic sensor data."
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default="sensor_data.log",
        help="Path to the log file (default: sensor_data.log)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval between sensor readings in seconds (default: 5)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="Duration to log data in seconds (default: run until stopped)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing log file instead of overwriting"
    )

    args = parser.parse_args()

    try:
        validate_args(args)
        logger = setup_logger(args.log_file, args.log_level)
        logger.info("Starting sensor data logging...")
        log_sensor_data(logger, args.interval, args.duration)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
