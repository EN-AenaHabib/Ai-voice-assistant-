import datetime
import requests
import re
import geocoder  # pip install geocoder

def get_weather(lat, lon, hour=None):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,weathercode&current_weather=true&timezone=auto"
    )
    try:
        data = requests.get(url).json()
        if hour is None:
            temp = data["current_weather"]["temperature"]
            return f"The current temperature is {temp}°C."
        else:
            times = data["hourly"]["time"]
            temps = data["hourly"]["temperature_2m"]
            for t, temp in zip(times, temps):
                t_hour = datetime.datetime.fromisoformat(t).hour
                if t_hour == hour:
                    return f"The temperature at {hour}:00 will be {temp}°C."
            return "Sorry, I couldn't find the weather for that hour."
    except Exception as e:
        return f"Error fetching weather: {e}"

def get_time_left(target_hour, target_minute=0):
    now = datetime.datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target_time < now:
        target_time += datetime.timedelta(days=1)
    diff = target_time - now
    hours, remainder = divmod(diff.seconds, 3600)
    minutes = remainder // 60
    return f"Time left for {target_hour}:{target_minute:02d} is {hours} hours and {minutes} minutes."

def assistant_reply(user_text):
    user_text = user_text.lower()

    # Get location
    g = geocoder.ip('me')
    lat, lon = g.latlng if g.ok else (None, None)

    if "time" in user_text and "left" not in user_text:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."

    if "time left" in user_text or "how much time" in user_text:
        match = re.search(r"(\d{1,2})(?::(\d{1,2}))?\s*(am|pm)?", user_text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            if match.group(3) == "pm" and hour != 12:
                hour += 12
            if match.group(3) == "am" and hour == 12:
                hour = 0
            return get_time_left(hour, minute)
        return "Please tell me the time you want to check."

    if "weather" in user_text and lat and lon:
        match = re.search(r"at\s*(\d{1,2})\s*(am|pm)?", user_text)
        if match:
            hour = int(match.group(1))
            if match.group(2) == "pm" and hour != 12:
                hour += 12
            if match.group(2) == "am" and hour == 12:
                hour = 0
            return get_weather(lat, lon, hour)
        return get_weather(lat, lon)

    return "I can currently tell you the time, time left until a specific hour, and the weather."

