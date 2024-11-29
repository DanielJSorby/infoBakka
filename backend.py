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
                return response.text
            return f"Error fetching Entur data: {response.status_code}, {response.text}"
    except httpx.TimeoutException as exc:
        return f"Timeout occurred: {exc}"
    except httpx.RequestError as exc:
        return f"Request error: {exc}"


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
    daily_forecasts = []
    seen_dates = set()

    for entry in data.get("properties", {}).get("timeseries", []):
        time_str = entry.get("time")
        if not time_str:
            continue

        timestamp = datetime.datetime.fromisoformat(time_str)
        date = timestamp.date()

        if date not in seen_dates:
            seen_dates.add(date)
            details = entry.get("data", {}).get("instant", {}).get("details", {})
            symbol_code = (
                entry.get("data", {})
                .get("next_1_hours", {})
                .get("summary", {})
                .get("symbol_code", None)
            )

            daily_forecasts.append(
                {
                    "date": date.isoformat(),
                    "time": time_str,
                    "details": details,
                    "symbol_code": symbol_code,
                }
            )

        if len(daily_forecasts) >= 7:
            break

    return json.dumps(daily_forecasts, indent=2)


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
