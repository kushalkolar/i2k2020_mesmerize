# get the roi manager
roi_manager = get_module('roi_manager')

# iterate through the roi list
for roi in roi_manager.manager.roi_list:
  # get the coordinates for an roi
  xs = roi.roi_xs
  ys = roi.roi_ys
  
  # create a 2D array of coordinates
  coors = np.column_stack([xs, ys])
  # get the centroid
  ctr = np.mean(coors, axis=0)

  # tag the ROI based on the centroid
  if ctr[0] > 250:
    roi.set_tag('cell_id', 'type_lt_100')
  else:
    roi.set_tag('cell_id', 'type_gt_100')
