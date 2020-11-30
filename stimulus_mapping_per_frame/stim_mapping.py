import pandas as pd
from mesmerize.plotting.utils import get_colormap

df = pd.read_csv('/home/kushal/i2k2020_data/I2K2020_testdata_AYUSO/Behavior2.csv')

# get the framerate of the video
fps = get_meta()['fps']

# multiply convert the units from seconds to frames
df['Time'] *= fps

# we need them as integer indices
df['Time'] = df['Time'].apply(int)

# NOTE: The above cannot be done in a 1 liner lambda in the Viewer script editor
# Keep your scripts very simple within a single scope, if you use functions 
# you cannot easily access the viewer work environment attributes within them

df['Behavior'] = df['Behavior'].fillna('nothing')

behavior_name_cmap = get_colormap(df['Behavior'].unique(), 'tab10', output='pyqt', alpha=0.6)

stim_mapping_df = pd.DataFrame(columns=['start', 'stop', 'name', 'color'])

for i, r in df.iterrows():
    if i == 0:
        start = r['Time']
        behavior = r['Behavior']
        continue
    
    if behavior != r['Behavior']:
        behavioral_period = pd.Series(
            {
                'start': int(start),
                'end': int(df.iloc[i-1]['Time']),
                'name': behavior,
                'color': behavior_name_cmap[behavior]
            }
        )
        stim_mapping_df = stim_mapping_df.append(behavioral_period, ignore_index=True)
        
        start = r['Time']
        behavior = r['Behavior']

# Trim off the behavior periods that are not in the current image sequence
trim = get_image().shape[2]
stim_mapping_df  = stim_mapping_df[stim_mapping_df['start'] <= trim]

smm = get_module('stimulus_mapping')

smm.maps['behavior'].set_data(stim_mapping_df)
