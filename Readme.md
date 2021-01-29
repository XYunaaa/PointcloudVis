#visualization in pointclouds 
Visualize point cloud in reflectivity or color by points or voxels；
## Example
Visualize contiguous frames' colored point clouds and storing them as video

![image](https://github.com/XYunaaa/PointcloudVis/blob/master/result/tracking19.gif)

Visualize point clouds by reflectivity

![image](https://github.com/XYunaaa/PointcloudVis/blob/master/result/原始点云_000185.png)

Visualize colored point clouds in voxels
![image](https://github.com/XYunaaa/PointcloudVis/blob/master/result/vexel_000185.png)

## Install
    main package : open3d 0.9.0 opencv-python mayavi
## Usage
    
    python draw_pc.py ; any environment with mayavi
    python draw_pc_colored.py; any environment with open3d0.9.0
    
    # Visualize point clouds by reflectivity
    import draw_pc
    # point clouds path
    raw_velo_path = 'data/185/原始点云000185.bin'
    non_ground_path = 'data/185/non_ground_000185.npy'
    # Load point clouds
    raw_vel_pc = np.fromfile(raw_velo_path,dtype=np.float32) # # bin type
    raw_vel_pc = raw_vel.reshape((-1,4))
    
    non_ground_pc = np.load(non_ground_path)   # npy type
    
    #  Visualization
    draw_pc.visualize_pts(raw_vel_pc)
    draw_pc.visualize_pts(non_ground_pc)


    #Visualize colored point clouds
    import draw_pc_colored.Plot as Plot
    ########Visualize colored point clouds in one frame######
    # Load point clouds
    non_ground_color_path = 'data/185/滤出地面的着色点云000185.npy'
    non_ground_color_pc = np.load(non_ground_color_path)
    #  Visualize colored point clouds
    Plot.draw_pc(non_ground_color_pc)
    #  if savefig=True will automatically save the image, 'name' is to save the path
    #  The para.json file holds the required camera perspective
    
    Plot.draw_pc(non_ground_color_pc,savefig=True,name='test.png')

    ########Visualize the continuous frame point cloud and save it to video######
    #  the continuous frame point cloud's path
    imgs_path = 'result/kitti_tracking/'
    seq = ['0020']
    for s in seq:
        imgs_path_seq = imgs_path + s +'/out_ps/'
        # stored video
        # If ps=False, the original image is directly stored into video, and ps=True, the brightness and contrast saturation of the image will be automatically adjusted, and the adjusted point cloud will be stored into video
        imgs2video(imgs_path_seq,ps=False)


    ######################################Visualize Voxel's  point cloud################################
    # Load
    non_ground_color_path = 'data/185/滤出地面的着色点云000185.npy'
    non_ground_color_pc = np.load(non_ground_color_path)
    #  Voxel is visualized and fills with color automatically
    Plot.draw_voxel(non_ground_color_pc)
