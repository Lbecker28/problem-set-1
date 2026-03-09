'''
You will run this problem set from main.py so set things up accordingly
'''
from src.transform_load import transform_and_load_data
from src.extract import extract_weather_data, extract_transit_data

# Call functions / instanciate objects from the two analysis .py files
def main():
    # Call functions from extract.py
    extract_weather_data()
    extract_transit_data()

    # Run transform + merge + EDA
    transform_and_load_data()

if __name__ == "__main__":
    main()
