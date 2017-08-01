import pandas as pd
import utilities as ut

# TODO
# Seperate latlng

df = pd.read_pickle('strava_data.p')

# Seperate Ride and Run data
df_run = df[df['type'] == 'Run']
df_ride = df[df['type'] == 'Ride']
print('Number of Run data entries: ', len(df_run))
print('Number of Ride data entries: ', len(df_ride))

# New pace column
df_run = ut.new_col_pace(df_run)

# Drop df_run outlier
df_run = ut.drop_outlier(df_run)

# New duration column
df_run = ut.new_col_duration(df_run)

# New zone column
df_run = ut.new_col_hr_zone(df_run)

# Save file as pickle
pd.to_pickle(df_run, 'df_run.p')
