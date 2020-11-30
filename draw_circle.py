import numpy as np

# just a function to generate some x-y coordinates
# r: radius
# n: number of points to return
def circle(r, n, x0, y0):
  import numpy as np # must be imported in local scope
  t = np.linspace(0, 2 * np.pi, n)
  x = r * np.cos(t)
  x += x0
  y = r * np.sin(t)
  y += y0
  return x, y

roi_manager = get_module('roi_manager')
roi_manager.start_backend('ScatterROI')

# get the coordinates for the ROI
xs, ys = circle(40, 50, 250, 300)

# generate some random curve data
curve_data = np.random.rand(8000)

# generate some data for dF/Fo and spikes (optional)
xlinspace = np.linspace(0, 8000, 8001)
dfof_data = np.sin(2 * np.pi * 10 * (xlinspace / 8001))
spike_data = np.cos(2 * np.pi * 10 * (xlinspace / 8001))

# add an ROI to the ROI manager
roi = roi_manager.manager.add_roi(
  curve=curve_data, 
  xs=xs,
  ys=ys,
  dfof_data=dfof_data,
  spike_data=spike_data
)

# set some tags to this newly created ROI
#roi.set_tag('cell_id', 'type_A')
#roi.set_tag('anatomical_location', 'rostral')

# You can basically do this in a loop to add all ROIs derived from an external source