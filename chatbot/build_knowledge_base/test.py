# import pandas as pd
# import random

# # Read CSV files
# circuits = pd.read_csv('./datasets/circuits.csv')
# constructor_results = pd.read_csv('./datasets/constructor_results.csv')
# constructor_standings = pd.read_csv('./datasets/constructor_standings.csv')
# constructors = pd.read_csv('./datasets/constructors.csv')
# driver_standings = pd.read_csv('./datasets/driver_standings.csv')
# drivers = pd.read_csv('./datasets/drivers.csv')
# lap_times = pd.read_csv('./datasets/lap_times.csv')
# pit_stops = pd.read_csv('./datasets/pit_stops.csv')
# qualifying = pd.read_csv('./datasets/qualifying.csv')
# races = pd.read_csv('./datasets/races.csv')
# results = pd.read_csv('./datasets/results.csv')
# sprint_results = pd.read_csv('./datasets/sprint_results.csv')
# status = pd.read_csv('./datasets/status.csv')

# # Function to replace IDs with real values
# def replace_ids_with_values(df, id_column, reference_df, reference_column):
#     print(f"Replacing IDs in {id_column} with real values from {reference_column} in {reference_df.shape[0]} rows")

#     # if already exists

#     new_df = df.copy()
#     new_df[id_column] = new_df[id_column].map(reference_df.set_index(id_column)[reference_column])
#     new_df.rename(columns={id_column: reference_column}, inplace=True)

#     df = new_df


# # Replace IDs with real values in each dataframe
# replace_ids_with_values(results, 'driverId', drivers, 'forename')
# replace_ids_with_values(results, 'constructorId', constructors, 'name')


# # replace_ids_with_values(constructor_results, 'constructorId', constructors, 'name')
# # replace_ids_with_values(constructor_standings, 'constructorId', constructors, 'name')
# # replace_ids_with_values(lap_times, 'driverId', drivers, 'forename')
# # replace_ids_with_values(pit_stops, 'driverId', drivers, 'forename')
# # replace_ids_with_values(qualifying, 'driverId', drivers, 'forename')
# # replace_ids_with_values(qualifying, 'constructorId', constructors, 'name')
# # replace_ids_with_values(races, 'circuitId', circuits, 'name')
# # replace_ids_with_values(results, 'driverId', drivers, 'forename')
# # replace_ids_with_values(results, 'constructorId', constructors, 'name')
# # replace_ids_with_values(sprint_results, 'driverId', drivers, 'forename')
# # replace_ids_with_values(sprint_results, 'constructorId', constructors, 'name')

# # Now, all IDs are replaced with their corresponding real values

import pandas as pd

# Read CSV files into DataFrames
circuits = pd.read_csv('./datasets/circuits.csv')
constructor_results = pd.read_csv('./datasets/constructor_results.csv')
constructor_standings = pd.read_csv('./datasets/constructor_standings.csv')
constructors = pd.read_csv('./datasets/constructors.csv')
driver_standings = pd.read_csv('./datasets/driver_standings.csv')
drivers = pd.read_csv('./datasets/drivers.csv')
lap_times = pd.read_csv('./datasets/lap_times.csv')
pit_stops = pd.read_csv('./datasets/pit_stops.csv')
qualifying = pd.read_csv('./datasets/qualifying.csv')
races = pd.read_csv('./datasets/races.csv')
results = pd.read_csv('./datasets/results.csv')
sprint_results = pd.read_csv('./datasets/sprint_results.csv')
status = pd.read_csv('./datasets/status.csv')

# Merge DataFrames based on common ID columns
merged_data = pd.merge(results, races, on='raceId')
merged_data = pd.merge(merged_data, circuits, on='circuitId')
merged_data = pd.merge(merged_data, drivers, on='driverId')
# Specify the columns to keep from the constructors DataFrame
merged_data = pd.merge(merged_data, constructors[['constructorId', 'name', 'nationality']], on='constructorId')
merged_data = pd.merge(merged_data, status, on='statusId', suffixes=('_result', '_status'))

# Replace IDs with real values
# For example, if you have a lookup table for driver IDs and names, you can use it to replace driver IDs with names.

# Save merged DataFrame to CSV
merged_data.to_csv('merged_data.csv', index=False)
