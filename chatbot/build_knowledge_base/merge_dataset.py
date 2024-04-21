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

# Save merged DataFrame to CSV
merged_data.to_csv('merged_data.csv', index=False)
