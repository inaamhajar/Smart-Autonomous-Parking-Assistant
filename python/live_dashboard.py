import serial
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
import time

PORT = 'COM7'
BAUD_RATE = 9600
WINDOW_SIZE = 100

RED_THRESHOLD = 10
YELLOW_THRESHOLD = 30
MAX_DISTANCE = 100

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # give Arduino time to reset after opening the port
ser.reset_input_buffer()

distances = deque(maxlen=WINDOW_SIZE)
timestamps = deque(maxlen=WINDOW_SIZE)
counter = 0

fig = plt.figure(figsize=(10, 7), facecolor='#0d1117')
fig.suptitle('SMART PARKING ASSISTANT — LIVE MONITOR', color='white',
             fontsize=14, fontweight='bold', y=0.98)

gauge_ax = fig.add_axes([0.1, 0.45, 0.8, 0.5])
gauge_ax.set_facecolor('#0d1117')
gauge_ax.axis('off')

graph_ax = fig.add_axes([0.1, 0.08, 0.8, 0.3])
graph_ax.set_facecolor('#161b22')
graph_ax.set_xlabel('Sample #', color='white')
graph_ax.set_ylabel('Distance (cm)', color='white')
graph_ax.tick_params(colors='white')
for spine in graph_ax.spines.values():
    spine.set_color('#30363d')

graph_line, = graph_ax.plot([], [], lw=2, color='#3fb950')
graph_ax.set_xlim(0, WINDOW_SIZE)
graph_ax.set_ylim(0, MAX_DISTANCE)


def zone_color(distance):
    if distance < RED_THRESHOLD:
        return '#f85149'
    elif distance < YELLOW_THRESHOLD:
        return '#d29922'
    else:
        return '#3fb950'


def zone_label(distance):
    if distance < RED_THRESHOLD:
        return 'DANGER — STOP'
    elif distance < YELLOW_THRESHOLD:
        return 'CAUTION'
    else:
        return 'CLEAR'


def draw_gauge(ax, distance):
    ax.clear()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.3)
    ax.axis('off')

    zones = [
        (0, RED_THRESHOLD, '#f85149'),
        (RED_THRESHOLD, YELLOW_THRESHOLD, '#d29922'),
        (YELLOW_THRESHOLD, MAX_DISTANCE, '#3fb950'),
    ]
    for start, end, color in zones:
        theta1 = 180 - (start / MAX_DISTANCE) * 180
        theta2 = 180 - (end / MAX_DISTANCE) * 180
        wedge = patches.Wedge((0, 0), 1.0, theta2, theta1,
                               width=0.25, facecolor=color, edgecolor='#0d1117')
        ax.add_patch(wedge)

    clamped = max(0, min(distance, MAX_DISTANCE))
    angle_deg = 180 - (clamped / MAX_DISTANCE) * 180
    angle_rad = np.radians(angle_deg)
    needle_x = 0.85 * np.cos(angle_rad)
    needle_y = 0.85 * np.sin(angle_rad)
    ax.plot([0, needle_x], [0, needle_y], color='white', lw=3, zorder=5)
    ax.add_patch(patches.Circle((0, 0), 0.05, color='white', zorder=6))

    color = zone_color(distance)
    ax.text(0, 0.55, f"{distance:.1f} cm", color=color, fontsize=26,
            fontweight='bold', ha='center', va='center')
    ax.text(0, 0.35, zone_label(distance), color=color, fontsize=13,
            fontweight='bold', ha='center', va='center')

    buzzer_on = distance < RED_THRESHOLD
    buzzer_color = '#f85149' if buzzer_on else '#30363d'
    buzzer_text = 'BUZZER ACTIVE' if buzzer_on else 'buzzer idle'
    ax.text(0, -0.1, buzzer_text, color=buzzer_color, fontsize=11,
            fontweight='bold', ha='center', va='center')


def read_latest_value():
    """Read all buffered lines and return only the most recent valid one,
    so the display always reflects the current distance, not a lagging queue."""
    latest = None
    while ser.in_waiting:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        if raw:
            try:
                latest = float(raw)
            except ValueError:
                print(f"Ignoring unparseable line: {raw!r}")
    return latest


def update(frame):
    global counter

    value = read_latest_value()
    if value is None:
        return graph_line,

    print(f"Reading: {value} cm")  # debug — watch this in the terminal

    distances.append(value)
    timestamps.append(counter)
    counter += 1

    draw_gauge(gauge_ax, value)

    graph_line.set_data(list(timestamps), list(distances))
    graph_line.set_color(zone_color(value))
    graph_ax.set_xlim(max(0, counter - WINDOW_SIZE), max(WINDOW_SIZE, counter))

    return graph_line,


if __name__ == '__main__':
    try:
        ani = FuncAnimation(fig, update, interval=100, blit=False)
        plt.show()
    finally:
        ser.close()