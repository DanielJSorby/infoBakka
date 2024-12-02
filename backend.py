import datetime
import json
from asyncio import sleep

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENTUR_API_URL = "https://api.entur.io/journey-planner/v3/graphql"
ENTUR_HEADERS = {
    "Content-Type": "application/json",
    "ET-Client-Name": "<infoBakka>-<InfoSkjerm>",
}
ENTUR_QUERY = """
{
  stopPlace(id: "NSR:StopPlace:6435") {
    id
    name
    estimatedCalls(timeRange: 60000, numberOfDepartures: 10) {
      realtime
      aimedArrivalTime
      aimedDepartureTime
      expectedArrivalTime
      expectedDepartureTime
      destinationDisplay {
        frontText
      }
      serviceJourney {
        journeyPattern {
          line {
            id
            name
          }
        }
      }
    }
  }
}

"""

YR_API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
YR_HEADERS = {
    "User-Agent": "infoBakka/1.0 (elvebakken@osloskolen.no)",
}
YR_LAT = 59.9139  # Oslo latitude
YR_LON = 10.7522  # Oslo longitude


async def fetch_entur_data():
    payload = {"query": ENTUR_QUERY, "variables": {}}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                ENTUR_API_URL, headers=ENTUR_HEADERS, json=payload
            )
            if response.status_code == 200:
                print("Entur API Response:", response.text)
                return response.text
            print(f"Error response: {response.status_code}, {response.text}")
            return f"Error fetching Entur data: {response.status_code}, {response.text}"
    except Exception as e:
        print(f"Exception in fetch_entur_data: {e}")
        return f"Error: {str(e)}"


async def fetch_yr_data():
    params = {"lat": YR_LAT, "lon": YR_LON}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(YR_API_URL, headers=YR_HEADERS, params=params)
            if response.status_code == 200:
                raw_data = response.json()
                return extract_daily_forecast(raw_data)
            return f"Error fetching Yr data: {response.status_code}, {response.text}"
    except httpx.TimeoutException as exc:
        return f"Timeout occurred: {exc}"
    except httpx.RequestError as exc:
        return f"Request error: {exc}"


def extract_daily_forecast(data):
    try:
        timeseries = data.get("properties", {}).get("timeseries", [])
        if not timeseries:
            return json.dumps({"error": "No weather data available"})

        current_weather = {}
        hourly_forecast = []

        # Get current weather
        current = timeseries[0]
        current_details = current.get("data", {}).get("instant", {}).get("details", {})
        current_symbol = (
            current.get("data", {})
            .get("next_1_hours", {})
            .get("summary", {})
            .get("symbol_code", "")
        )

        current_weather = {
            "temperature": round(current_details.get("air_temperature", 0)),
            "wind_speed": round(current_details.get("wind_speed", 0)),
            "symbol": current_symbol,
            "precipitation": current.get("data", {})
                .get("next_1_hours", {})
                .get("details", {})
                .get("precipitation_amount", 0)
        }

        # Get next 24 hours forecast
        for entry in timeseries[:24]:  # Next 24 hours
            time = entry.get("time")
            details = entry.get("data", {}).get("instant", {}).get("details", {})
            symbol = (
                entry.get("data", {})
                .get("next_1_hours", {})
                .get("summary", {})
                .get("symbol_code", "")
            )
            precipitation = (
                entry.get("data", {})
                .get("next_1_hours", {})
                .get("details", {})
                .get("precipitation_amount", 0)
            )

            hour = datetime.datetime.fromisoformat(time).strftime("%H")
            
            forecast_entry = {
                "hour": hour,
                "temperature": round(details.get("air_temperature", 0)),
                "symbol": symbol,
                "precipitation": precipitation
            }
            hourly_forecast.append(forecast_entry)

        return json.dumps({
            "current": current_weather,
            "hourly": hourly_forecast
        }, indent=2)
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return json.dumps({"error": f"Error processing weather data: {str(e)}"})


async def generate_entur_data():
    while True:
        data = await fetch_entur_data()
        yield f"{data}\n\n"
        await sleep(10)


async def generate_yr_data():
    while True:
        data = await fetch_yr_data()
        yield f"{data}\n\n"
        await sleep(10)


@app.get("/data")
async def get_entur_data():
    return StreamingResponse(generate_entur_data(), media_type="text/event-stream")


@app.get("/weather")
async def get_yr_data():
    return StreamingResponse(generate_yr_data(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
