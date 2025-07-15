from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import os
from datetime import datetime, timedelta

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = os.getenv("API_KEY", "")
UNITS = os.getenv("MOEPAGE_WEATHER_UNITS", "metric")
CITY = os.getenv("CITY", "Semarang")


@app.get("/", response_class=HTMLResponse)
def get_weather(request: Request, city: str = Query(CITY)):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}&lang=id"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={UNITS}&lang=id"

    weather_data = {}
    forecast_data = []
    local_time = "Tidak diketahui"

    try:
        res = requests.get(weather_url)
        res.raise_for_status()
        weather_data = res.json()

        res = requests.get(forecast_url)
        res.raise_for_status()
        forecast_all = res.json()
        forecast_data = forecast_all.get("list", [])[::8]

        timezone_offset = weather_data.get("timezone", 0)
        local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)
        local_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

    except Exception as e:
        pass 

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": weather_data,
        "forecast": forecast_data,
        "local_time": local_time
    })
