import requests
import json
from datetime import datetime
from secretapi import api

url = "https://api.sl.se/api2/realtimedeparturesV4.json?key={}&siteid=9112&timewindow=20".format(api)

response = requests.get(url)
json_obj = json.loads(response.text)

metros = json_obj["ResponseData"]["Metros"]

south_metros = [m for m in metros if m["JourneyDirection"] == 2]
print(json.dumps(south_metros  , indent=4))


results = []
for metro in south_metros:
    time_stamp = metro["DisplayTime"]
    if time_stamp == "Nu":
        continue

    if " " in time_stamp:
        time_stamp = time_stamp.split(" ")[0]

    results.append(time_stamp)

now = datetime.now()
current_hour = now.hour
current_minute = now.minute
print("The time is " + str(current_hour) + ":" + str(current_minute))
print(results)
