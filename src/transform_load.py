'''
PART 2: Merge and transform the data
- Read in the two datasets from /data into two separate dataframes
- Profile, clean, and standardize date fields for both as needed
- Merge the two dataframe for the date range 10/1/2024 - 10/31/2025
- Conduct EDA to understand the relationship between weather and transit ridership over time
-- Create a line plot of daily transit ridership and daily average temperature over the whole time period
-- For February 2025, create a scatterplot of daily transit ridership vs. precipitation
-- Create a correlation heatmap of all numeric features in the merged dataframe
-- Load the merged dataframe as a CSV into /data
-- In a print statement, summarize any interesting trends you see in the merged dataset
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def transform_and_load_data(
    transit_path="data/transit_data.csv",
    weather_path="data/weather_data.csv",
    output_path="data/merged_transit_weather.csv",
):
    """
    Reads transit and weather data, cleans and merges them by date,
    performs required EDA, saves the merged CSV, and returns the merged dataframe.
    """

    # Read datasets
    transit_df = pd.read_csv(transit_path)
    weather_df = pd.read_csv(weather_path)

    # Clean and standardize date columns
    transit_df["service_date"] = pd.to_datetime(
        transit_df["service_date"], errors="coerce"
    )
    weather_df["datetime"] = pd.to_datetime(
        weather_df["datetime"], errors="coerce"
    )

    # Restrict date range
    start_date = pd.to_datetime("2024-10-01")
    end_date = pd.to_datetime("2025-10-31")

    transit_df = transit_df[
        (transit_df["service_date"] >= start_date)
        & (transit_df["service_date"] <= end_date)
    ].copy()

    weather_df = weather_df[
        (weather_df["datetime"] >= start_date)
        & (weather_df["datetime"] <= end_date)
    ].copy()

    # Standardize date column names
    transit_df = transit_df.rename(columns={"service_date": "date"})
    weather_df = weather_df.rename(columns={"datetime": "date"})

    # Merge datasets
    merged_df = pd.merge(transit_df, weather_df, on="date", how="inner")
    merged_df = merged_df.sort_values("date").copy()

    # Line plot of daily ridership and daily average temperature
    fig, ax1 = plt.subplots(figsize=(14, 6))

    ax1.plot(
        merged_df["date"],
        merged_df["total_rides"],
        label="Daily Transit Ridership",
        color="blue",
    )
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Transit Ridership", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.plot(
        merged_df["date"],
        merged_df["temp"],
        label="Daily Avg Temp",
        color="red",
    )
    ax2.set_ylabel("Average Temperature", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    plt.title("Daily Transit Ridership and Average Temperature Over Time")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.tight_layout()
    plt.savefig("data/daily_ridership_temp.png")
    plt.close()

    # February 2025 scatterplot of ridership vs precipitation
    feb_2025 = merged_df[
        (merged_df["date"] >= "2025-02-01")
        & (merged_df["date"] <= "2025-02-28")
    ].copy()

    plt.figure(figsize=(8, 6))
    plt.scatter(feb_2025["precip"], feb_2025["total_rides"], alpha=0.7)
    plt.xlabel("Daily Precipitation")
    plt.ylabel("Daily Transit Ridership")
    plt.title("February 2025: Transit Ridership vs Precipitation")

    plt.tight_layout()
    plt.savefig("data/feb_2025_ridership_precip.png")
    plt.close()

    # Correlation heatmap of numeric features
    numeric_df = merged_df.select_dtypes(include="number").drop(
        columns=["tzoffset", "transit_id", "weather_id"],
        errors="ignore",
    )

    if not numeric_df.empty:
        corr_matrix = numeric_df.corr()

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=False,
            cmap="coolwarm",
            center=0,
            linewidths=0.5,
        )
        plt.title("Correlation Heatmap of Numeric Features")

        plt.tight_layout()
        plt.savefig("data/correlation_heatmap.png")
        plt.close()

    # Save merged dataframe
    merged_df.to_csv(output_path, index=False)

    # Print summary of trends
    print(
            "A comparison of Chicago transit ridership and weather data reveals several interesting trends. "
    "Ridership seems to follow seasonal patters, with more riders taking transit during warmer months and"
    "less riders taking transit during colder months. Additionally, precipitation appears to have a weaker relationship with "
    "ridership (from viewing a scatterplot in February), though heavy rain may slightly reduce "
    "ridership levels. Overall, the relationship between temperature has a very noticeable relationship with "
    "ridership, possibly due to seasonal trends."
    )

    return merged_df