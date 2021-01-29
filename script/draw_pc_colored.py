import open3d as o3d
import numpy as np
import colorsys, random
import os
# show pc with aimed color(label/aimed rgb)
def save_view_point(pc, filename):
    pc_colored = pc.copy()
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(pc_colored[:, 0:3])
    # pc_normals = np.zeros((pc_xyzrgb.shape[0],3)) + 10
    # pc.normals = open3d.utility.Vector3dVector(pc_normals)
    if pc_colored.shape[1] == 3:
        o3d.draw_geometries([pc])
        return 0
    if np.max(pc_colored[:, 3:6]) > 20:  ## 0-255
        pc.colors = o3d.utility.Vector3dVector(pc_colored[:, 3:6] / 255.)
    else:
        pc.colors = o3d.utility.Vector3dVector(pc_colored[:, 3:6])

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pc)
    vis_control = vis.get_view_control()
    vis.run()
    param = vis_control.convert_to_pinhole_camera_parameters()
    o3d.io.write_pinhole_camera_parameters(filename, param)
    vis_control.scale(-8)
    vis.destroy_window()
    vis.close()

class Plot:

    @staticmethod
    def random_colors(N, bright=True, seed=0):
        brightness = 1.0 if bright else 0.7
        hsv = [(0.15 + i / float(N), 1, brightness) for i in range(N)]
        colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
        random.seed(seed)
        return colors

    @staticmethod
    def draw_pc(pc_xyzrgb,savefig=False,name=None):

        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(pc_xyzrgb[:, 0:3])
        #pc_normals = np.zeros((pc_xyzrgb.shape[0],3)) + 10
        #pc.normals = open3d.utility.Vector3dVector(pc_normals)
        if pc_xyzrgb.shape[1] == 3:
            o3d.draw_geometries([pc])
            return 0
        if np.max(pc_xyzrgb[:, 3:6]) > 20:  ## 0-255
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6] / 255.)
        else:
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6])
        if not savefig:
            vis = o3d.visualization.Visualizer()
            vis.create_window()
            vis_control = vis.get_view_control()
            param = o3d.io.read_pinhole_camera_parameters('para.json')
            vis.add_geometry(pc)
            vis_control.convert_from_pinhole_camera_parameters(param)
            vis.poll_events()
            vis.update_renderer()
            vis.run()
            return 0
        else:

            vis = o3d.visualization.Visualizer()
            vis.create_window()
            vis_control = vis.get_view_control()
            #save_view_point(pc,'para1.json') # 调整到满意的视角后 按q退出 该视角信息被保存在para.json下; 再次运行程序将该行代码注释掉
            param = o3d.io.read_pinhole_camera_parameters('para.json')
            vis.add_geometry(pc)
            vis_control.convert_from_pinhole_camera_parameters(param)
            ''' for open3d >=0.10.0
            front = [ -0.9917820008427326, -0.06773734865811093, 0.10853623542925953 ]
            lookat = [ 39.381500244140625, 1.1175003051757812, 0.69850003719329834 ]
            up = [ 0.10261310693082715, 0.085530815590998441, 0.99103735039116536 ]
            zoom = 0.379
            vis_control.set_front(front)
            vis_control.set_lookat(lookat)
            vis_control.set_up(up)
            vis_control.set_zoom(zoom)
            '''
            #vis_control.rotate(x=1,y=1)
            #vis_control.set_zoom(0.75)
            #vis_control.translate(x=-1,y=-50)
            #param = vis_control.convert_to_pinhole_camera_parameters()
            #o3d.io.write_pinhole_camera_parameters('para.json',param)
            #
            #vis.update_geometry()
            #vis_control.scale(-8)
            vis.poll_events()
            vis.update_renderer()
            vis.run()
            vis.capture_screen_image(name)
            vis.destroy_window()
            vis.close()
            #image = cv2.imread('test.png')
            #image = image[200:-200,200:-500,:]
            #cv2.imwrite(name,image)
            return 0



    @staticmethod
    def draw_voxel(pc_xyzrgb):
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(pc_xyzrgb[:, 0:3])
        # pc_normals = np.zeros((pc_xyzrgb.shape[0],3)) + 10
        # pc.normals = open3d.utility.Vector3dVector(pc_normals)
        if pc_xyzrgb.shape[1] == 3:
            o3d.draw_geometries([pc])
            return 0
        if np.max(pc_xyzrgb[:, 3:6]) > 20:  ## 0-255
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6] / 255.)
        else:
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6])
        voxel_size = 0.18
        voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pc, voxel_size)
        o3d.visualization.draw_geometries([voxel_grid])

    @staticmethod
    def draw_bbox(bboxes):
        lines_list = []
        corners_3d_list = []
        for bbox in bboxes:
            ## draw each box's corner and line
            bbox = np.array(bbox)
            lines = [[0, 1], [1, 2], [2,3],[3,0],[0, 4], [1, 5], [2,6],[3,7],[4,5], [5, 6], [6,7],[7,4]]
            colors = [[255,0,0] for i in range(len(lines))]
            colors_corner = [[255, 0, 0] for i in range(len(bbox))]
            ## define 8 corners of bboxes3d ##
            corners_3d_bbox = o3d.geometry.PointCloud()
            corners_3d_bbox.points = o3d.utility.Vector3dVector(bbox)
            corners_3d_bbox.colors = o3d.utility.Vector3dVector(colors_corner)
            ## define bbox3d's lines ##
            lines_bbox = o3d.geometry.LineSet()
            lines_bbox.lines = o3d.utility.Vector2iVector(lines)
            lines_bbox.colors = o3d.utility.Vector3dVector(colors)
            lines_bbox.points = o3d.utility.Vector3dVector(bbox)

            corners_3d_list.append(corners_3d_bbox)
            lines_list.append(lines_bbox)

        return lines_list, corners_3d_list

    @staticmethod
    def draw_pc_bbox(pc_xyzrgb,bboxes,savefig=False,name=None):

        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(pc_xyzrgb[:, 0:3])
        lines_list, corners_3d_list = Plot.draw_bbox(bboxes)


        if pc_xyzrgb.shape[1] == 3:
            o3d.draw_geometries([pc])
            return 0
        if np.max(pc_xyzrgb[:, 3:6]) > 20:  ## 0-255
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6] / 255.)
        else:
            pc.colors = o3d.utility.Vector3dVector(pc_xyzrgb[:, 3:6])

        visual_set = [pc]
        for i in range(len(corners_3d_list)):
            visual_set.append(corners_3d_list[i])
            visual_set.append(lines_list[i])

        if not savefig:

            vis = o3d.visualization.Visualizer()
            vis.create_window()
            vis_control = vis.get_view_control()
            Plot.save_view_point(pc, 'para1.json')  # 调整到满意的视角后 按q退出 该视角信息被保存在para.json下; 再次运行程序将该行代码注释掉
            param = o3d.io.read_pinhole_camera_parameters('para.json')
            vis.add_geometry(visual_set)
            vis_control.convert_from_pinhole_camera_parameters(param)
            vis.poll_events()
            vis.update_renderer()
            vis.run()
            return 0
        else:

            vis = o3d.visualization.Visualizer()
            vis.create_window()
            vis_control = vis.get_view_control()
            Plot.save_view_point(pc, 'para1.json')  # 调整到满意的视角后 按q退出 该视角信息被保存在para.json下; 再次运行程序将该行代码注释掉
            param = o3d.io.read_pinhole_camera_parameters('para.json')
            vis.add_geometry(visual_set)
            vis_control.convert_from_pinhole_camera_parameters(param)
            vis.poll_events()
            vis.update_renderer()
            vis.run()
            vis.capture_screen_image(name)
            vis.destroy_window()
            vis.close()
            return 0


path = '/media/ddd/data2/3d_MOTS_Ex./Figs/传感器融合/result/kitti_tracking/0019'
path = '/media/ddd/data3/RGBPoints/npy/'
outpath = 'result/kitti_tracking/0019/out'
if not os.path.exists(outpath):
    os.makedirs(outpath)

for _,_,file_list in os.walk(path):
    for f in file_list:
        num = f.split('.')[0]
        outpath_f = outpath+num+'.png'
        pc = np.load(path+f)

        #pc = np.fromfile(path+f,dtype=np.float32)
        #pc = pc.reshape((-1,7)) # x y z i r g b

        pc_copy = pc.copy()
        pc[:, 3] = pc_copy[:,-1]
        pc[:, 4] = pc_copy[:,5]
        pc[:, 5] = pc_copy[:,4]
        pc[:, -1] = pc_copy[:,3]
        save_view_point(pc, 'para.json')  # 调整到满意的视角后 按q退出 该视角信息被保存在para.json下; 再次运行程序将该行代码注释掉
        #不保存
        #Plot.draw_pc(pc, savefig=False) # pc xyzbgri
        #保存图像
        Plot.draw_pc(pc,savefig=True,name=outpath_f)



