# Import glob so we can get all tiff files in a dir
from glob import glob
# Import os to get filenames from paths
import os

# Motion correction params.

mc_kwargs = \
{
    "max_shifts":           (48, 8),
    "niter_rig":            3,
    "max_deviation_rigid":  3,
    "strides":              (128, 128),
    "overlaps":             (64, 64),
    "upsample_factor_grid": 6,
    "gSig_filt":            (32, 32)  # Set to `None` for 2p data
}



params = \
{
    'mc_kwargs':        mc_kwargs,  # the kwargs we set above
    'item_name':        "will set later per file",
    'output_bit_depth': "Do not convert"  # can also set to `8` or `16` if you want the output in `8` or `16` bit
}

# Path to the dir containing images
files = glob("/home/kushal/i2k2020_data/I2K2020_testdata_AYUSO/*.tif")
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

    # Get caiman motion correction module, hide=False to not show GUI
    mc_module = get_module("caiman_motion_correction", hide=True)

    # Set name for this video file
    name = os.path.basename(path)[:-4]
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
