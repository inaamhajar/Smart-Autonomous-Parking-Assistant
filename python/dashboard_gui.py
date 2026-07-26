import tkinter as tk
import random



window = tk.Tk()

window.title("Smart Parking Assistant")

window.geometry("500x400")



title = tk.Label(
    window,
    text="Smart Parking Assistant",
    font=("Arial",20)
)

title.pack(pady=20)



distance_label = tk.Label(
    window,
    text="Distance:",
    font=("Arial",18)
)

distance_label.pack()



status_label = tk.Label(
    window,
    text="Status:",
    font=("Arial",18)
)

status_label.pack()



def update_sensor():


    distance = random.randint(5,100)


    if distance > 50:
        status = "SAFE"

    elif distance > 20:
        status = "WARNING"

    else:
        status = "STOP"



    distance_label.config(
        text=f"Distance: {distance} cm"
    )


    status_label.config(
        text=f"Status: {status}"
    )


    window.after(
        1000,
        update_sensor
    )



update_sensor()


window.mainloop()