'''
PART 1: EXTRACT WEATHER AND TRANSIT DATA

Pull in data from two dataset
1. Weather data from visualcrossing's weather API (https://www.visualcrossing.com/weather-api)
- You will need to sign up for a free account to get an API key
-- You only get 1000 rows free per day, so be careful to build your query correctly up front
-- Though not best practice, include your API key directly in your code for this assignment
- Write code below to get weather data for Chicago, IL for the date range 10/1/2024 - 10/31/2025
- The default data fields should be sufficient
2. Daily transit ridership data for the Chicago Transit Authority (CTA)
- Here is the URL: ttps://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

Load both as CSVs into /data
- Make sure your code is line with the standards we're using in this class 
'''

#Write your code below
import io
from pathlib import Path

import pandas as pd
import requests


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


# Extract visual crossing weather data for Chicago, IL
import urllib.request
import json

# Define API endpoint and parameters
location = "Chicago,IL"
api_key = "GEREPXFMPRGDCSL5N3M4NBTHE"
unit_group = "metric"
start_date = "2024-10-01"
end_date = "2025-10-31"
content_type = "json"

# Construct the API URL
import requests
import pandas as pd


def extract_weather_data() -> pd.DataFrame:

    location = "Chicago,IL"
    api_key = "GEREPXFMPRGDCSL5N3M4NBTHE"
    unit_group = "metric"
    start_date = "2024-10-01"
    end_date = "2025-10-31"
    content_type = "json"

    api_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{location}/{start_date}/{end_date}"
        f"?unitGroup={unit_group}&include=days&contentType=json&key={api_key}"
    )

    response = requests.get(api_url)
    response.raise_for_status()

    weather_json = response.json()

    # Convert JSON daily records into dataframe
    weather_df = pd.DataFrame(weather_json["days"])

    # Create unique ID (required by assignment)
    weather_df["weather_id"] = weather_df.index + 1

    # Save to CSV
    weather_df.to_csv("data/weather_data.csv", index=False)

    return weather_df
# Extract CTA transit ridership data
def extract_transit_data() -> pd.DataFrame:

    transit_url = "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

    transit_df = pd.read_csv(transit_url)

    transit_df["transit_id"] = transit_df.index + 1

    transit_df.to_csv(DATA_DIR / "transit_data.csv", index=False)

    return transit_df