import json
from asyncio import sleep

import httpx
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Entur API settings
ENTUR_API_URL = "https://api.entur.io/journey-planner/v3/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "ET-Client-Name": "<infoBakka>-<InfoSkjerm>",
}

# GraphQL query
QUERY = """
{
  stopPlace(
    id: "NSR:StopPlace:6435"
  ) {
    id
    name
    estimatedCalls(
      timeRange: 60000,
      numberOfDepartures: 10
    ) {
      realtime
      aimedArrivalTime
      aimedDepartureTime
      expectedArrivalTime
      expectedDepartureTime
      actualArrivalTime
      actualDepartureTime
      date
      forBoarding
      forAlighting
      destinationDisplay {
        frontText
      }
      quay {
        id
      }
      serviceJourney {
        journeyPattern {
          line {
            id
            name
            transportMode
          }
        }
      }
    }
  }
}
"""


# Fetch data from the Entur API
async def fetch_entur_data():
    payload = {"query": QUERY, "variables": {}}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(ENTUR_API_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                return response.text
            else:
                return f"Error fetching data: {response.status_code}, {response.text}"
    except httpx.TimeoutException as exc:
        return f"Timeout occurred: {exc}"
    except httpx.RequestError as exc:
        return f"Request error: {exc}"


# Streaming response to send data every 10 seconds
async def generate_entur_data():
    while True:
        data = await fetch_entur_data()
        yield f"{data}\n\n"
        await sleep(10)  # Wait for 10 seconds before the next request


# API endpoint to stream data from the Entur API
@app.get("/data")
async def get_entur_data():
    return StreamingResponse(generate_entur_data(), media_type="text/event-stream")


# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
