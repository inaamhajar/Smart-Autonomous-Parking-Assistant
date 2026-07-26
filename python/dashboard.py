import random
import time


print("Smart Parking Assistant Started")


while True:

    distance = random.randint(5, 100)


    if distance > 50:
        status = "SAFE"


    elif distance > 20:
        status = "WARNING"


    else:
        status = "STOP"



    print(
        "Distance:",
        distance,
        "cm | Status:",
        status
    )


    time.sleep(1)