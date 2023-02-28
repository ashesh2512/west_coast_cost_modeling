import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
os.chdir('/Users/asharma/codes/P_Code/currTests/west_coast_cost_modeling/west_coast_sites/')

plot_based_on = 'phase'
start_date  = '01/01/2010'
start_date = pd.to_datetime(start_date)

# read excel sheet and drop irrelevant stuff
df = pd.read_excel('north_ca_actions.xlsx')
df = df.drop('cost_multiplier', axis=1)
df = df.drop('level', axis=1)
df = df.drop('location', axis=1)
df = df.drop('phase_name', axis=1)
df = df.drop('max_waveheight', axis=1)
df = df.drop('max_windspeed', axis=1)
df = df.drop('transit_speed', axis=1)
df = df.drop('num_vessels', axis=1)

# sort based on time
df = df.sort_values('time', ascending=True)

# create a new column converting time to date-time
start_date_list = []
end_date_list = []
for idx in range(0, df.shape[0]):
    end_date_list.append(start_date + pd.DateOffset(hours=df.loc[idx].at['time'])) #specify the number of hours and add it to start_date
    start_date_list.append(start_date + pd.DateOffset(hours=df.loc[idx].at['time']) \
                           - pd.DateOffset(hours=df.loc[idx].at['duration'])) #specify the number of hours and add it to start_date
    

# add dates column to the data frame 
df.insert(loc = 5, column = 'start_date', value = start_date_list)
df.insert(loc = 6, column = 'end_date', value = end_date_list)

# create additional data for gantt charts
df['days_to_start'] = (df['start_date'] - df['start_date'].min()).dt.days
df['days_to_end'] = (df['end_date'] - df['start_date'].min()).dt.days
df['phase_duration'] = df['days_to_end'] - df['days_to_start'] + 1

# print(df)
df.to_excel("north_ca_action_gantt.xlsx", index=False)

# we will change phase name to delay if delay appears in the agent
for idx in range(0, df.shape[0]):
    if 'Delay' in df.at[idx, 'action']:
        df.at[idx, plot_based_on] = 'Delay'

################################# Plot based on Phases #################################
unique_phases = df[plot_based_on].unique()
# print(unique_phases)

# assign colors for phases/agents
def color(row):
    if plot_based_on == 'agent':
        c_dict = {unique_phases[0]:'#228B22', unique_phases[1]:'#00FFFF', unique_phases[2]:'#76EEC6', unique_phases[3]:'#000000', \
                  unique_phases[4]:'#1E90FF', unique_phases[5]:'#8B7D6B', unique_phases[6]:'#0000FF', unique_phases[7]:'#8A2BE2', \
                  unique_phases[8]:'#A52A2A', unique_phases[9]:'#FF6103', unique_phases[10]:'#7FFF00', unique_phases[11]:'#FF1493', \
                  unique_phases[12]:'#8B7500'}
        return c_dict[row['agent']]
    elif plot_based_on == 'phase':
        c_dict = {unique_phases[0]:'#228B22', unique_phases[1]:'#00FFFF', unique_phases[2]:'#000000', unique_phases[3]:'#76EEC6', \
                  unique_phases[4]:'#1E90FF', unique_phases[5]:'#8B7D6B'}
        return c_dict[row[plot_based_on]]
df['color'] = df.apply(color, axis=1)

fig, ax = plt.subplots(1, figsize=(16,6))
left_spacing = 0.3
ax.barh(y=df[plot_based_on], width=df['phase_duration'], left=df['days_to_start'], color=df.color)
plt.title('Full project installation schedule for North CA reference site from ' + (df['start_date'].min()).strftime("%m/%d/%y") + ' to ' + (df['end_date'].max()).strftime("%m/%d/%y"))
xticks_labels = pd.date_range(start=df['start_date'].min(), end=df['end_date'].max()).strftime("%m/%d/%y")
ax.set_xticklabels(xticks_labels[::100])
plt.gca().invert_yaxis()
fig.subplots_adjust(left=left_spacing)
plt.show()