import tkinter as tk
import random
import csv
import os
from datetime import datetime

# ----------------------------
# Create Data folder if needed
# ----------------------------
os.makedirs("Data", exist_ok=True)

csv_file = "Data/distance_log.csv"

# Create CSV header only if file doesn't exist
new_file = not os.path.exists(csv_file)

file = open(csv_file, "a", newline="")
writer = csv.writer(file)

if new_file:
    writer.writerow(["Time", "Distance (cm)", "Status"])

# ----------------------------
# Create Window
# ----------------------------
window = tk.Tk()

window.title("Smart Autonomous Parking Assistant")
window.geometry("500x450")

# ----------------------------
# Title
# ----------------------------
title = tk.Label(
    window,
    text="Smart Autonomous Parking Assistant",
    font=("Arial", 20, "bold")
)

title.pack(pady=20)

# ----------------------------
# Distance Label
# ----------------------------
distance_text = tk.Label(
    window,
    text="Distance",
    font=("Arial", 16)
)

distance_text.pack()

number_label = tk.Label(
    window,
    text="0 cm",
    font=("Arial", 42, "bold")
)

number_label.pack(pady=15)

# ----------------------------
# Status Label
# ----------------------------
status_label = tk.Label(
    window,
    text="Status",
    font=("Arial", 18, "bold")
)

status_label.pack()

# ----------------------------
# Recommendation Label
# ----------------------------
message_label = tk.Label(
    window,
    text="",
    font=("Arial", 16)
)

message_label.pack(pady=20)

# ----------------------------
# Update Function
# ----------------------------
def update_sensor():

    # Fake sensor value
    distance = random.randint(5, 100)

    # Parking logic
    if distance > 50:
        status = "SAFE"
        color = "green"
        message = "Keep moving forward"

    elif distance > 20:
        status = "WARNING"
        color = "orange"
        message = "Slow down"

    else:
        status = "STOP"
        color = "red"
        message = "STOP!"

    # Update GUI
    number_label.config(text=f"{distance} cm")

    status_label.config(
        text=f"Status: {status}",
        fg=color
    )

    message_label.config(
        text=message
    )

    # Save to CSV
    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        distance,
        status
    ])

    file.flush()

    # Update every second
    window.after(1000, update_sensor)

# Start updates
update_sensor()

# Keep window open
window.mainloop()

# Close CSV file when program exits
file.close()