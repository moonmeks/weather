from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
import requests
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=j1&lang=ru"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Ошибка при получении данных"}

    data = response.json()
    current = data["current_condition"][0]
    return {
        "city": city,
        "temp": current["temp_C"] + "°C",
        "feels": current["FeelsLikeC"] + "°C",
        "desc": current["lang_ru"][0]["value"],
        "wind": current["windspeedKmph"] + " км/ч",
        "humidity": current["humidity"] + "%"
    }


@app.get("/weather")
def weather_api(city: str = Query(..., description="Название города")):
    return get_weather(city)

@app.get("/", response_class=HTMLResponse)
def index(request: Request, city: str = None):
    weather = None
    if city:
        weather = get_weather(city)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "weather": weather, "city": city}
    )
