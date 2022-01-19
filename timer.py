from datetime import datetime
import time


update = 10
while True:
    t = time.strftime("%S")
    print(t)

    time.sleep(update)
