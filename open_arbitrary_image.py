import numpy as np
# open a numpy
a = np.load('/home/kushal/i2k2020_data/pvc7/image.npy')

# create a meta data dict, these are the minimal required keys
meta = \
{
  'origin': 'my_microscope',
  'date': '20201204_121234',
  'fps': 25.0,
}

# create an ImgData object with the image and metadata
imgdata = ImgData(a.T, meta)

# create a new work environment with the ImgData
workenv = ViewerWorkEnv(imgdata)

# set the new work env
vi.viewer.workEnv = workenv

# update the GUI
update_workEnv()
