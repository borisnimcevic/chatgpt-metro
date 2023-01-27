import requests
import json
from datetime import datetime
from secretapi import api

url = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=9112&timewindow=30".format(api)
import time

while True:
    response = requests.get(url)
    json_obj = json.loads(response.text)

    metros = json_obj["ResponseData"]["Metros"]

    south_metros = [m for m in metros if m["JourneyDirection"] == 2]

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
# print("The time is " + str(current_hour) + ":" + str(current_minute))

    current_time = "{}:{}".format(current_hour,current_minute)
# print(current_time)

    results = []
    for metro in south_metros:
        time_stamp = metro["DisplayTime"]
        if time_stamp == "Nu":
            continue

        if " " in time_stamp:
            time_stamp = time_stamp.split(" ")[0]

        if ":" in time_stamp:
            time1_obj = datetime.strptime(current_time, "%H:%M")
            time2_obj = datetime.strptime(time_stamp, "%H:%M")
            time_diff = time2_obj - time1_obj
            time_stamp = int(time_diff.total_seconds() / 60)

        results.append(int(time_stamp))

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
# print(results)

    walking_time = 7;
    packing_time = 5;
    total_time_offset = walking_time + packing_time

    time_to_leave = 99;
    for num in results:
        if num > total_time_offset :
            time_to_leave = num - total_time_offset  - 1; # one min room for error
            # if(time_to_leave == 0):
            #     print("Leave NOW!")
            # else:
            #     print("Leave in " + str(time_to_leave) + " min.")
            break

    with open("a.txt", "w") as f:
        f.write(str(time_to_leave))
    time.sleep(20)

