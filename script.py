import pandas as pd
import os

ORIGINAL_DATA_FOLDER = "original_datasets/"

# File paths
locations_file = os.path.join(ORIGINAL_DATA_FOLDER, "46_bird_survey_locations.csv")
surveys_file = os.path.join(ORIGINAL_DATA_FOLDER, "46_bird_surveys.csv")
observations_file = os.path.join(ORIGINAL_DATA_FOLDER, "46_bird_observations.csv")

# Load the datasets
locations_df = pd.read_csv(locations_file)
surveys_df = pd.read_csv(surveys_file)
observations_df = pd.read_csv(observations_file)

### DATA CLEANING ###

# Clean Bird Survey Locations Data
locations_df['lat'] = pd.to_numeric(locations_df['lat'], errors='coerce')
locations_df['long'] = pd.to_numeric(locations_df['long'], errors='coerce')
locations_df['begin_date'] = pd.to_datetime(locations_df['begin_date'], errors='coerce')
locations_df['end_date'] = pd.to_datetime(locations_df['end_date'], errors='coerce')
locations_df = locations_df.dropna(subset=['lat', 'long'])  # Drop rows with missing location data

# Clean Bird Surveys Data
surveys_df['survey_date'] = pd.to_datetime(surveys_df['survey_date'], errors='coerce')
surveys_df['time_start'] = pd.to_datetime(surveys_df['time_start'], errors='coerce').dt.time
surveys_df['time_end'] = pd.to_datetime(surveys_df['time_end'], errors='coerce').dt.time
surveys_df.fillna({"wind_speed": 0, "air_temp": surveys_df["air_temp"].median()}, inplace=True)  # Fill missing values
surveys_df = surveys_df.drop_duplicates()  # Remove duplicates

# Clean Bird Observations Data
observations_df['survey_date'] = pd.to_datetime(observations_df['survey_date'], errors='coerce')
observations_df['bird_count'] = pd.to_numeric(observations_df['bird_count'], errors='coerce')
observations_df['bird_count'].fillna(1, inplace=True)
observations_df = observations_df.dropna(subset=['common_name'])

# Cleaned Data
CLEAN_DATA_FOLDER = "cleaned_datasets/"

locations_df.to_csv(os.path.join(CLEAN_DATA_FOLDER, "cleaned_bird_survey_locations.csv"), index=False)
surveys_df.to_csv(os.path.join(CLEAN_DATA_FOLDER, "cleaned_bird_surveys.csv"), index=False)
observations_df.to_csv(os.path.join(CLEAN_DATA_FOLDER, "cleaned_bird_observations.csv"), index=False)