#!/usr/bin/env python3
import argparse
import time
import sys
import board
import busio
import adafruit_bme280
from typing import Optional

def initialize_i2c_sensor(address: int = 0x77) -> adafruit_bme280.Adafruit_BME280:
    """Initialize an I2C BME280 sensor."""
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bme280.Adafruit_BME280(i2c, address=address)
        return sensor
    except Exception as e:
        print(f"Error initializing I2C sensor: {str(e)}", file=sys.stderr)
        sys.exit(1)

def initialize_spi_sensor(cs_pin: str = "CE0") -> adafruit_bme280.Adafruit_BME280:
    """Initialize an SPI BME280 sensor."""
    try:
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        cs = board.__getattribute__(cs_pin)
        sensor = adafruit_bme280.Adafruit_BME280(spi, cs)
        return sensor
    except Exception as e:
        print(f"Error initializing SPI sensor: {str(e)}", file=sys.stderr)
        sys.exit(1)

def read_sensor_data(sensor) -> dict:
    """Read data from the sensor."""
    try:
        return {
            "temperature": round(sensor.temperature, 2),  # Celsius
            "humidity": round(sensor.humidity, 2),        # Percentage
            "pressure": round(sensor.pressure, 2)         # hPa
        }
    except Exception as e:
        print(f"Error reading sensor data: {str(e)}", file=sys.stderr)
        return None

def print_sensor_data(data: dict, sensor_type: str, timestamp: str) -> None:
    """Print sensor data to terminal with formatted output."""
    if data:
        print(f"[{timestamp}] {sensor_type} Sensor Data:")
        print(f"  Temperature: {data['temperature']} °C")
        print(f"  Humidity: {data['humidity']} %")
        print(f"  Pressure: {data['pressure']} hPa")
        print("-" * 40)
    else:
        print(f"[{timestamp}] Error: No data received from sensor.")

def main():
    """Main function to parse arguments and monitor sensor data."""
    parser = argparse.ArgumentParser(
        description="CLI-based sensor monitor for I2C/SPI sensors."
    )
    parser.add_argument(
        "--interface",
        type=str,
        choices=["i2c", "spi"],
        default="i2c",
        help="Sensor interface type (i2c or spi, default: i2c)"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Interval between sensor readings in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        help="Duration to monitor sensor in seconds (default: run until stopped)"
    )
    parser.add_argument(
        "--address",
        type=lambda x: int(x, 0),  # Handle hex input (e.g., 0x77)
        default=0x77,
        help="I2C address in hex (default: 0x77)"
    )
    parser.add_argument(
        "--cs-pin",
        type=str,
        default="CE0",
        help="SPI chip select pin (default: CE0)"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.interval <= 0:
        print("Error: Interval must be a positive number.", file=sys.stderr)
        sys.exit(1)
    if args.duration is not None and args.duration <= 0:
        print("Error: Duration must be a positive number.", file=sys.stderr)
        sys.exit(1)

    # Initialize sensor
    sensor = None
    sensor_type = args.interface.upper()
    if args.interface == "i2c":
        sensor = initialize_i2c_sensor(args.address)
    elif args.interface == "spi":
        sensor = initialize_spi_sensor(args.cs_pin)

    # Monitor sensor
    start_time = time.time()
    try:
        while True:
            if args.duration and (time.time() - start_time) > args.duration:
                print("Monitoring duration reached. Stopping.")
                break

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            data = read_sensor_data(sensor)
            print_sensor_data(data, sensor_type, timestamp)
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
