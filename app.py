import requests
import urllib.parse

from dateutil import tz
from datetime import datetime, timezone
from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Global datetime
sgtz = tz.gettz('Asia/Singapore')
now = datetime.now(tz=sgtz).isoformat(timespec='seconds')
today = datetime.now(tz=sgtz).strftime('%Y-%m-%d')
nicenow = datetime.now(tz=sgtz).strftime('%-I:%M%p, %-d %b %Y')

avgtemp = 0
avghumid = 0
s_no = []


def rtwget(url_t, url_h):

    # Get temperature data
    try:
        tempResponse = requests.get(url_t)
        tempResponse.raise_for_status()

    except requests.RequestException:
        return {
            "id": "No station ID available",
            "name": "",
            "tempvalue": "NA",
            "humidity": "NA",
            "h_index": "NA",
            "index": "1",
        }

    # Get humidity data
    try:
        humidityResponse = requests.get(url_h)
        humidityResponse.raise_for_status()

    except requests.RequestException:
        return {
            "id": "No station ID available",
            "name": "",
            "tempvalue": "NA",
            "humidity": "NA",
            "h_index": "NA",
            "index": "1",
        }

    # Send data to parse function
    data = rtwparse(tempResponse.json(), humidityResponse.json())

    return data


def rtwparse(tempData, humidityData):

    # Lists to calculate averages
    temp = []
    humid = []
    
    # List of dicts to store station data
    rtw_data = []

    # Parse data
    try:

        # Get station data
        station_list = tempData["metadata"]["stations"]
        for station in station_list:
            station_data = {
                "id": station["id"],
                "name": station["name"],
            }
            rtw_data.append(station_data)

        if len(station_list) >= 14:
            # Loaded all, find most up to date data list with all stations
            # as latest data may not have all stations
            for item in reversed(tempData["items"]):
                if len(item["readings"]) >= 14:
                    currentData_t = item["readings"]
                    break

            for item in reversed(humidityData["items"]):
                if len(item["readings"]) >= 14:
                    currentData_h = item["readings"]
                    break

        else:
            # Not load all, may not have all stations
            currentData_t = tempData["items"][0]["readings"]
            currentData_h = humidityData["items"][0]["readings"]


        for index, station in enumerate(rtw_data):
            station["tempvalue"] = currentData_t[index]["value"]
            station["humidity"] = currentData_h[index]["value"]
            station["h_index"] = h_index(currentData_t[index]["value"], currentData_h[index]["value"])
            station["index"] = index + 1
            s_no.append(index + 1)
            temp.append(currentData_t[index]["value"])
            humid.append(currentData_h[index]["value"])

        global avgtemp
        avgtemp = sum(temp)/len(temp)

        global avghumid
        avghumid = sum(humid)/len(humid)

        return rtw_data

    except (KeyError, TypeError, ValueError):
        return {
            "id": "No station ID available",
            "name": "",
            "tempvalue": "NA",
            "humidity": "NA",
            "h_index": "NA",
            "index": "1",
        }


def uvi():

    # Get data
    try:
        url = f"https://api.data.gov.sg/v1/environment/uv-index?date_time={urllib.parse.quote(now)}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.RequestException:
        return {
            "time": "NA", #latest UVI reading time
            "value": "NA" #latest UVI reading
        }

    # Parse data
    try:
        data = response.json()

        return {
            "time": data["items"][0]["index"][0]["timestamp"], #latest UVI reading time
            "value": data["items"][0]["index"][0]["value"] #latest UVI reading
        }

    except (KeyError, TypeError, ValueError):
        return {
            "time": "NA", #latest UVI reading time
            "value": "NA" #latest UVI reading
        }


def avgdata():

    avgdata = []

    # No avg temp data
    if not avgtemp:
        avgdata.extend(("Hot/cold?", "Yes/no?"))
        return avgdata

    # Append appropriate average temp phrase to first list item
    if avgtemp >= 32.0:
        avgdata.append("Now damn hot,")
    elif avgtemp >= 30.0:
        avgdata.append("Now quite hot,")
    elif avgtemp >= 28.0:
        avgdata.append("Now not so hot,")
    else:
        avgdata.append("Now not hot,")
    
    # No avg humidity data
    if not avghumid:
        avgdata.append("not sure if humid or not?")
        return avgdata

    # Append appropriate average humidity phrase to second list item
    if avghumid >= 90.0:
        avgdata.append("damn humid!")
    elif avghumid >= 80.0:
        avgdata.append("quite humid!")
    elif avghumid >= 60.0:
        avgdata.append("not so humid!")
    else:
        avgdata.append("not humid!")

    return avgdata


def h_index(temp, humid):
    # Formula constants
    C1 = -8.78469475556
    C2 = 1.61139411
    C3 = 2.33854883889
    C4 = -0.14611605
    C5 = -0.012308094
    C6 = -0.0164248277778
    C7 = 0.002211732
    C8 = 0.00072546
    C9 = -0.000003582

    # Heat index formula
    hi = C1 + (C2 * temp) + (C3 * humid) + (C4 * temp * humid) + (C5 * (temp ** 2)) + (C6 * (humid ** 2)) + (C7 * (temp ** 2) * humid) + (C8 * temp * (humid ** 2)) + (C9 * (temp ** 2) * (humid ** 2))
    
    return round(hi, 1)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Load only most recent data
        url_t = f"https://api.data.gov.sg/v1/environment/air-temperature?date_time={urllib.parse.quote(now)}"
        url_h = f"https://api.data.gov.sg/v1/environment/relative-humidity?date_time={urllib.parse.quote(now)}"


    if request.method == "POST":
        # Load latest data with all stations
        url_t = f"https://api.data.gov.sg/v1/environment/air-temperature?date={urllib.parse.quote(today)}"
        url_h = f"https://api.data.gov.sg/v1/environment/relative-humidity?date={urllib.parse.quote(today)}"

    rtw = rtwget(url_t, url_h)
    avg = avgdata()

    return render_template("index.html", rtw=rtw, avg=avg, uvi=uvi(), s_no=s_no, time=nicenow)
