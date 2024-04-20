import pandas as pd
import random

# Read CSV files
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

# Function to replace IDs with real values
def replace_ids_with_values(df, id_column, reference_df, reference_column):
    df[id_column] = df[id_column].map(reference_df.set_index(id_column)[reference_column])
    df.rename(columns={id_column: reference_column}, inplace=True)
    
    # get df filename
    df_filename = random.randint(1, 100)


    # save the dataframe to a new CSV file
    df.to_csv(f'./datasets/newfiles/{df_filename}.csv', index=False)

# Replace IDs with real values in each dataframe
replace_ids_with_values(constructor_results, 'constructorId', constructors, 'name')
replace_ids_with_values(constructor_standings, 'constructorId', constructors, 'name')
replace_ids_with_values(lap_times, 'driverId', drivers, 'forename')
replace_ids_with_values(pit_stops, 'driverId', drivers, 'forename')
replace_ids_with_values(qualifying, 'driverId', drivers, 'forename')
replace_ids_with_values(qualifying, 'constructorId', constructors, 'name')
replace_ids_with_values(races, 'circuitId', circuits, 'name')
replace_ids_with_values(results, 'driverId', drivers, 'forename')
replace_ids_with_values(results, 'constructorId', constructors, 'name')
replace_ids_with_values(sprint_results, 'driverId', drivers, 'forename')
replace_ids_with_values(sprint_results, 'constructorId', constructors, 'name')

# Now, all IDs are replaced with their corresponding real values
