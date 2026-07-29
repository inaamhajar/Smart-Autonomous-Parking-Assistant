import serial
import csv
import os
from datetime import datetime

PORT = 'COM7'
BAUD_RATE = 9600
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'distance_log.csv')


def main():
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {PORT} at {BAUD_RATE} baud. Logging to {OUTPUT_FILE}")
    print("Press Ctrl+C to stop.")

    file_exists = os.path.isfile(OUTPUT_FILE)

    with open(OUTPUT_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'distance_cm'])

        try:
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    try:
                        distance_value = float(line)
                    except ValueError:
                        continue

                    timestamp = datetime.now().isoformat()
                    writer.writerow([timestamp, distance_value])
                    f.flush()
                    print(f"{timestamp} - {distance_value} cm")
        except KeyboardInterrupt:
            print("\nLogging stopped by user.")
        finally:
            ser.close()


if __name__ == '__main__':
    main()