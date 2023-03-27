import numpy as np
import pandas as pd
import sys

import os
os.chdir('/Users/asharma/codes/P_Code/currTests/west_coast_cost_modeling/west_coast_sites/')

# problem parameters
site = 'southern_WA'
port = 'Grays_Harbor'
start_date  = '01/01/2020'
start_date = pd.to_datetime(start_date)
phase_name = 'MooredSubInstallation'
unique_delays = True

# read excel sheet and drop irrelevant stuff
df = pd.read_excel('scenario_actions/' + site + '_action_' + port + '_' + start_date.strftime('%m_%d_%Y') + '.xlsx')

# keep only rows corresponding to the phase of interest
df = df[df['phase'] == phase_name]
df_delay = df.loc[:, ['action', 'duration', 'time']].copy()
df_delay = df_delay.rename(columns={'time': 'end_time'})
df_delay = df_delay[df_delay['action'] == 'Delay']

# sort based on time
df = df.sort_values('time', ascending=True)
df = df.reset_index(drop = True)
df_delay = df_delay.sort_values('end_time', ascending=True)
df_delay = df_delay.reset_index(drop = True)

# create start times 
df_delay['start_time'] = df_delay['end_time'] - df_delay['duration']
df_delay = df_delay.sort_values('start_time', ascending=True)
df_delay = df_delay.reset_index(drop = True)
df_delay = df_delay.reindex(columns=['action', 'start_time', 'duration', 'end_time'])

# add dummy row at end
new_row = pd.DataFrame({
    'action': ['Delay'],
    'start_time': [sys.float_info.max],
    'duration': [0],
    'end_time': [sys.float_info.max]
})
df_delay = df_delay.append(new_row, ignore_index=True)

# remove weather delay rows that are overlapping with other weather delays
if (unique_delays):
    idx = 0
    while (idx < df_delay.shape[0]-1):
        delay_end = df_delay.at[idx, 'start_time'] + df_delay.at[idx, 'duration']
        if (delay_end >= df_delay.at[idx+1, 'end_time']):
            df_delay = df_delay.drop(index=idx+1)
            df_delay = df_delay.reset_index(drop = True)
            continue
        elif ((delay_end > df_delay.at[idx+1, 'start_time']) and (delay_end < df_delay.at[idx+1, 'end_time'])):
            df_delay.at[idx, 'end_time'] = df_delay.at[idx+1, 'end_time']
            df_delay.at[idx, 'duration'] = df_delay.at[idx, 'end_time'] - df_delay.at[idx, 'start_time']
            df_delay = df_delay.drop(index=idx+1)
            df_delay = df_delay.reset_index(drop = True)
        idx += 1

weather_delays = df_delay['duration'].sum()
print(f"\nWeather Delays: {weather_delays:.3f} hrs")

first_process = df['duration'].loc[df['time'].idxmin()]
phase_duration = df['time'].max() - df['time'].min() + first_process
print(f"Phase Duration: {phase_duration:.3f} hrs")

efficiency = (phase_duration - weather_delays)/phase_duration
print(f"Efficiency: {efficiency*100:.3f}%\n")
