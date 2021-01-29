#import open3d
import numpy as np
import colorsys, random
from mayavi import mlab

# show point clouds with reflectivity
def visualize_pts(pts, fig=None, bgcolor=(0, 0, 0), fgcolor=(1.0, 1.0, 1.0),
                  show_intensity=True, size=(600, 600), draw_origin=True):
    if not isinstance(pts, np.ndarray):
        pts = pts.cpu().numpy()
    if fig is None:
        fig = mlab.figure(figure=None, bgcolor=bgcolor, fgcolor=fgcolor, engine=None, size=size)

    if show_intensity:
        G = mlab.points3d(pts[:, 0], pts[:, 1], pts[:, 2], pts[:, 3],scale_mode="none",
                         scale_factor=0.15, figure=fig)
    else:
        G = mlab.points3d(pts[:, 0], pts[:, 1], pts[:, 2], scale_mode="none",
                          colormap='gnuplot', scale_factor=0.2, figure=fig)
    if draw_origin:
        mlab.points3d(0, 0, 0, color=(1, 1, 1), mode='cube', scale_factor=0.2)
        mlab.plot3d([0, 3], [0, 0], [0, 0], color=(0, 0, 1), tube_radius=0.1)
        mlab.plot3d([0, 0], [0, 3], [0, 0], color=(0, 1, 0), tube_radius=0.1)
        mlab.plot3d([0, 0], [0, 0], [0, 3], color=(1, 0, 0), tube_radius=0.1)

    mlab.show()

    return fig


## read data ##
#raw_velo_path = 'data/185/原始点云000185.bin'
non_ground_path = 'data/185/non_ground_000185.npy'
non_ground_path = 'data/003352.npy'
#non_ground_fov_path = 'data/185/non_ground_000185_fov.npy'
non_ground_fov_path = '/media/ddd/data3/RGBPoints/bin/000000.bin'
##Load
raw_vel = np.fromfile(non_ground_fov_path,dtype=np.float32)
raw_vel = raw_vel.reshape((-1,4))
#non_ground_pc = np.load(non_ground_path)
#non_ground_pc_fov = np.load(non_ground_fov_path)

## show ##
#visualize_pts(non_ground_pc_fov)
visualize_pts(raw_vel)
#visualize_pts(non_ground_pc)


