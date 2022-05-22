from time import sleep


from datetime import datetime
import os
while True:
    print(datetime.now())
    os.system("python3 ./bot.py")
    sleep(120)