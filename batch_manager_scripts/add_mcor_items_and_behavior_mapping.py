# Import glob so we can get all tiff files in a dir
from glob import glob
# Import os to get filenames from paths
import os

import pandas as pd
from mesmerize.plotting.utils import get_colormap

# Motion correction params.

mc_kwargs = \
    {
        "max_shifts": (48, 8),
        "niter_rig": 3,
        "max_deviation_rigid": 3,
        "strides": (128, 128),
        "overlaps": (64, 64),
        "upsample_factor_grid": 6,
        "gSig_filt": (32, 32)  # Set to `None` for 2p data
    }

params = \
    {
        'mc_kwargs': mc_kwargs,  # the kwargs we set above
        'item_name': "will set later per file",
        'output_bit_depth': "Do not convert"  # can also set to `8` or `16` if you want the output in `8` or `16` bit
    }

# Path to the dir containing images
files = glob("/work/kushal/i2k2020/I2K2020_testdata_AYUSO/*.tif")
# Sort in alphabetical order (should also work for numbers)
files.sort()

# Open each file, crop, and add to batch with 3 diff mot cor params
for i, path in enumerate(files):
    print("Working on file " + str(i + 1) + " / " + str(len(files)))

    # get json file path for the meta data
    meta_path = path[:-4] + ".json"

    # Create a new work environment with this image sequence
    work_env = ViewerWorkEnv.from_tiff(path, "asarray", meta_path, meta_format="json_minimal")

    # set it as the current work environment
    vi.viewer.workEnv = work_env
    vi.update_workEnv()

    # name of the video file, use the same name for the csv behavior file	
    name = os.path.basename(path)[:-4]
    df = pd.read_csv(f'/work/kushal/i2k2020/I2K2020_testdata_AYUSO/{name}.csv')

    # get the framerate of the video
    fps = get_meta()['fps']

    # multiply convert the units from seconds to frames
    df['Time'] *= fps

    # we need them as integer indices
    df['Time'] = df['Time'].apply(int)

    # NOTE: The above cannot be done in a 1 liner lambda in the Viewer script editor
    # Keep your scripts very simple within a single scope, if you use functions 
    # you cannot easily access the viewer work environment attributes within them

    df['Behavior'] = df['Behavior'].fillna('nothing')  # fill in the unlabelled frames

    behavior_name_cmap = get_colormap(df['Behavior'].unique(), 'tab10', output='pyqt', alpha=0.6)  # map the behaviors to colors

    stim_mapping_df = pd.DataFrame(columns=['start', 'stop', 'name', 'color'])  # create an empty stimmap dataframe

    for i, r in df.iterrows():  # This loop converts "per-frame" labelled behaviors to "chunk-labelled" with start and end frame numbers for each behavioral period
        if i == 0:
            start = r['Time']
            behavior = r['Behavior']
            continue

        if behavior != r['Behavior']:
            behavioral_period = pd.Series(
                {
                    'start': int(start),
                    'end': int(df.iloc[i - 1]['Time']),
                    'name': behavior,
                    'color': behavior_name_cmap[behavior]
                }
            )
            stim_mapping_df = stim_mapping_df.append(behavioral_period, ignore_index=True)

            start = r['Time']
            behavior = r['Behavior']

    # Trim off the behavior periods that are not in the current image sequence
    trim = get_image().shape[2]
    stim_mapping_df = stim_mapping_df[stim_mapping_df['start'] <= trim]

    smm = get_module('stimulus_mapping')

    smm.maps['behavior'].set_data(stim_mapping_df)

    # Get caiman motion correction module, hide=False to not show GUI
    mc_module = get_module("caiman_motion_correction", hide=True)

    # Set name for this video file
    params["item_name"] = name
    ##########################################################
    # First variant of params
    params["mc_kwargs"]["gSig_filt"] = (32, 32)
    params["mc_kwargs"]["strides"] = (128, 128)
    params["mc_kwargs"]["overlaps"] = (64, 64)

    # Add one variant of params for this video to the batch
    mc_module.add_to_batch(params)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (26, 26)
    mc_module.add_to_batch(params)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (20, 20)
    mc_module.add_to_batch(params)
    
    ##########################################################
    # Try another variant of params
    params["mc_kwargs"]["gSig_filt"] = (32, 32)
    params["mc_kwargs"]["strides"] = (96, 96)
    params["mc_kwargs"]["overlaps"] = (48, 48)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (26, 26)
    mc_module.add_to_batch(params)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (20, 20)
    mc_module.add_to_batch(params)
    
    ##########################################################
    # Try another variant of params
    params["mc_kwargs"]["gSig_filt"] = (32, 32)
    params["mc_kwargs"]["strides"] = (64, 64)
    params["mc_kwargs"]["overlaps"] = (32, 32)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (26, 26)
    mc_module.add_to_batch(params)
    
    # another variant with diff gSig
    params["mc_kwargs"]["gSig_filt"] = (20, 20)
    mc_module.add_to_batch(params)
