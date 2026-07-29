


# Smart Autonomous Parking Assistant 

A real-time object-detection system built with an Arduino ultrasonic sensor, tiered LED/buzzer alerts, and a Python-based data pipeline for logging, live visualization, and anomaly detection.

## Video Demo 
https://github.com/user-attachments/assets/b9c1a78f-d701-41ff-81cd-e1d5cb9a91c2

## Authors

Inaam HAJAR - https://github.com/inaamhajar
Yasmine BERNARD - https://github.com/jasobernnn

## Features

- Real-time distance measurement using an HC-SR04 ultrasonic sensor
- Tiered visual alerts: green (safe), yellow (caution), red (danger)
- Audible buzzer alert triggered in the danger zone
- Serial communication between Arduino and Python
- Python data logging pipeline (CSV output with timestamps)
- Live-updating distance graph with color-coded zones
- Rolling statistical anomaly detection on sensor readings

## Tech Stack

- **Hardware:** Arduino Uno, HC-SR04 ultrasonic sensor, LEDs, passive buzzer
- **Firmware:** C++ (Arduino)
- **Software:** Python, pyserial, matplotlib
- **Tools:** Git, GitHub


## How It Works

1. The Arduino continuously measures distance using the ultrasonic sensor's pulse timing.
2. Based on the measured distance, it switches between three zones:
   - **< 10 cm** → Red LED + buzzer (danger)
   - **10–30 cm** → Yellow LED (caution)
   - **> 30 cm** → Green LED (safe)
3. Distance readings are sent over serial to a connected computer.
4. Python scripts read this serial stream to either log readings to CSV or display a live, color-coded graph with anomaly detection.

## Setup

### 1. Upload the Arduino sketch

Open `arduino/distance_sensor.ino` in the Arduino IDE and upload it to your board.

### 2. Wire the components

| Component        | Arduino Pin |
|-------------------|-------------|
| Ultrasonic Trig   | 10 |
| Ultrasonic Echo   | 9  |
| Red LED           | 2  |
| Yellow LED        | 7  |
| Green LED         | 8  |
| Buzzer            | 11 |

### 3. Install Python dependencies

```bash
cd python
pip install -r requirements.txt
```

### 4. Run the logger or live dashboard

Update the `PORT` variable in the scripts if your Arduino isn't on COM7.

```bash
python serial_logger.py
```

or

```bash
python live_dashboard.py
```

## Future Improvements

- Web-based dashboard using Flask for remote monitoring
- Configurable thresholds via a config file or CLI arguments
- Data export/analysis notebook using pandas
- Support for multiple sensors simultaneously
