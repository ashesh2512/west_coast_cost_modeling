import datetime as dt
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
import numpy as np
import pandas as pd
import textwrap

import os
os.chdir('/Users/asharma/codes/P_Code/currTests/west_coast_cost_modeling/west_coast_sites/')
write_mode = False

# problem parameters
site = 'central_CA'
port = 'San_Luis'
start_date  = '01/01/2020'
start_date = pd.to_datetime(start_date)
plot_based_on = 'agent'

# read excel sheet and drop irrelevant stuff
df = pd.read_excel('scenario_actions/' + site + '_action_' + port + '_' + start_date.strftime('%m_%d_%Y') + '.xlsx')
df = df.drop('cost_multiplier', axis=1)
df = df.drop('level', axis=1)
df = df.drop('phase_name', axis=1)
df = df.drop('max_waveheight', axis=1)
df = df.drop('max_windspeed', axis=1)
df = df.drop('transit_speed', axis=1)
df = df.drop('num_vessels', axis=1)
df = df.drop('num_ahts_vessels', axis=1)
df = df.drop(df[df['action'] == 'Onshore Construction'].index)
df = df.drop(df[df['action'] == 'Mobilize'].index)

# sort based on time
df = df.sort_values('time', ascending=True)
df = df.reset_index(drop = True)

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

# we will change phase name to delay if delay appears in the agent
for idx in range(0, df.shape[0]):
    if 'Delay' == df.at[idx, 'action']:
        df.at[idx, plot_based_on] = 'Delay: Weather'
    elif 'Delay' in df.at[idx, 'action'] and 'Delay' != df.at[idx, 'action']:
        df.at[idx, plot_based_on] = df.at[idx, 'action']

if write_mode:
    df.to_excel('scenario_actions/' + site + '_action_gantt_' + port + '_' + start_date.strftime('%m_%d_%Y') + '.xlsx', index=False)

################################# Change the name of Agents #################################

for idx in range(0, df.shape[0]):
    if df.at[idx, 'agent'] == 'Mooring System Installation Vessel':
        df.at[idx, 'agent'] = 'Mooring System Installation'
    elif df.at[idx, 'agent'] == 'Export Cable Installation Vessel':
        df.at[idx, 'agent'] = 'Export Cable Installation'
    elif df.at[idx, 'agent'] == 'Array Cable Installation Vessel':
        df.at[idx, 'agent'] = 'Array Cable Installation'
    elif df.at[idx, 'agent'] == 'Towing Group 1':
        df.at[idx, 'agent'] = 'Floating Turbine Installation Group 1'
    elif df.at[idx, 'agent'] == 'Towing Group 2':
        df.at[idx, 'agent'] = 'Floating Turbine Installation Group 2'
    elif df.at[idx, 'agent'] == 'Towing Group 3':
        df.at[idx, 'agent'] = 'Floating Turbine Installation Group 3'
    elif df.at[idx, 'agent'] == 'Floating Substation Installation Vessel':
        df.at[idx, 'agent'] = 'Floating Substation Installation'

################################# Plot based on Phases/Agents #################################
df[plot_based_on] = df[plot_based_on].str.wrap(30)
unique_phases = df[plot_based_on].unique()
# print(unique_phases)

agent_dic = ['Mooring System Installation', 'Export Cable Installation', 'Array Cable Installation', \
             'Floating Turbine Installation Group 1', 'Floating Turbine Installation Group 2', 'Floating Turbine Installation Group 3','Floating Substation Installation', \
             'Substation Assembly Line 1', 'Substructure Assembly Line 1', 'Turbine Assembly Line 1', 'Substructure Assembly Line 2', 'Turbine Assembly Line 2', \
             'Delay: Waiting on Substation Assembly', 'Delay: No Substructures in Wet Storage', 'Delay: No Substructure Storage Available', 'Delay: No Completed Turbine Assemblies', 'Delay: No Assembly Storage Available', \
             'Delay: Weather']
wrapped_agent_dic = [textwrap.fill(phrase, width=30) for phrase in agent_dic]

# assign colors for phases/agents
def color(row):
    if plot_based_on == 'agent':
        c_dict = {wrapped_agent_dic[0]:'#EEEE00', wrapped_agent_dic[1]:'#EE0000', wrapped_agent_dic[2]:'#8B0000', \
                  wrapped_agent_dic[3]:'#7FFF00', wrapped_agent_dic[4]:'#66CD00', wrapped_agent_dic[5]:'#458B00', wrapped_agent_dic[6]:'#EE9A49', \
                  wrapped_agent_dic[7]:'#8B5A2B', wrapped_agent_dic[8]:'#AB82FF', wrapped_agent_dic[9]:'#4876FF', wrapped_agent_dic[10]:'#5D478B', wrapped_agent_dic[11]:'#27408B', \
                  wrapped_agent_dic[12]:'#9E9E9E', wrapped_agent_dic[13]:'#9E9E9E', wrapped_agent_dic[14]:'#9E9E9E', wrapped_agent_dic[15]:'#9E9E9E', wrapped_agent_dic[16]:'#9E9E9E', \
                  wrapped_agent_dic[17]:'#000000'}
        return c_dict[row['agent']]
    elif plot_based_on == 'phase':
        c_dict = {unique_phases[0]:'#228B22', unique_phases[1]:'#00FFFF', unique_phases[2]:'#76EEC6', unique_phases[3]:'#000000', \
                  unique_phases[4]:'#1E90FF', unique_phases[5]:'#8B7D6B', unique_phases[6]:'#0000FF', unique_phases[7]:'#8A2BE2', \
                  unique_phases[8]:'#A52A2A', unique_phases[9]:'#483D8B'}
        return c_dict[row[plot_based_on]]
df['color'] = df.apply(color, axis=1)

fig, ax = plt.subplots(1, figsize=(8,7))
ax.barh(y=df[plot_based_on], width=df['phase_duration'], left=df['days_to_start'], color=df.color)
# plt.title('Full project installation schedule for North CA reference site from ' + (df['start_date'].min()).strftime("%m/%d/%y") + ' to ' + (df['end_date'].max()).strftime("%m/%d/%y"))

num_x_labels = 5
day_spacing = int(((df['end_date'].max() - df['start_date'].min()).days)/num_x_labels)
xticks = np.arange(0, df['days_to_end'].max()+1, day_spacing)
ax.set_xticks(xticks)
ax.set_xlabel("Days elapsed since the start of installation")
# xticks_labels = pd.date_range(start=df['start_date'].min(), end=df['end_date'].max()).strftime("%m/%d/%y")
# ax.set_xticklabels(xticks_labels[::day_spacing])

plt.gca().invert_yaxis()
fig.subplots_adjust(left=0.32)

plt.show()