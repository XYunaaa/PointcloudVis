#import open3d
import os, sys
import cv2
import numpy as np
import argparse

imgs_path = 'result/kitti_tracking/0019/'
target_size = (1920, 1080)
target_fps = 8.0
# 输出文件名
target_video = 'out.mp4'
# 是否保存 resize 的中间图像
saveResizeFlag = False
img_types = ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')

import cv2
import imutils
import numpy as np

def contract_and_bright(img,c,b):
    # after test ,c =11 b=6 is better
    cnum = c
    bnum = b
    cimg = np.ones((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            lst = 0.1*cnum*img[i, j] + bnum
            cimg[i, j] = [int(ele) if ele < 255 else 255 for ele in lst]
    return cimg

def s_and_b(hlsImg,l,s):
    lsImg = np.zeros(hlsImg.shape, np.float32)
    hlsCopy = np.copy(hlsImg)
    l = l
    s = s
    MAX_VALUE = 100
    # 1.调整亮度饱和度(线性变换)、 2.将hlsCopy[:,:,1]和hlsCopy[:,:,2]中大于1的全部截取
    hlsCopy[:, :, 1] = (1.0 + l / float(MAX_VALUE)) * hlsCopy[:, :, 1]
    hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1
    # HLS空间通道2是饱和度，对饱和度进行线性变换，且最大值在255以内，这一归一化了，所以应在1以内
    hlsCopy[:, :, 2] = (1.0 + s / float(MAX_VALUE)) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    return lsImg

def imgs2video(imgs_path,ps =True):
    output_path = imgs_path + 'out/'
    output_ps_path = imgs_path + 'out_ps/'
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(output_ps_path):
        os.mkdir(output_ps_path)
    target_path = output_path + target_video

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(target_path, fourcc, target_fps, target_size)

    images = os.listdir(imgs_path)
    images = sorted(images)
    count = 0
    for image in images:
        if not (image.lower().endswith(img_types)):
            continue
        try:
            print(image)
            frame = cv2.imdecode(np.fromfile(imgs_path + image, dtype=np.uint8),
                                 cv2.IMREAD_COLOR)  # , cv2.IMREAD_UNCHANGED
            if ps:
                frame = contract_and_bright(frame,11,10)
                # 图像归一化，且转换为浮点型, 颜色空间转换 BGR转为HLS
                fImg = frame.astype(np.float32)
                fImg = fImg / 255.0
                # HLS空间，三个通道分别是: Hue色相、lightness亮度、saturation饱和度
                # 通道0是色相、通道1是亮度、通道2是饱和度
                hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
                frame = s_and_b(hlsImg,20,50)
                cv2.imwrite(output_ps_path+image,frame*255)
            # 写入视频
            vw.write(frame)
            count += 1
        except Exception as exc:
            print(image, exc)
    vw.release()
    print('\r\nConvert Success! Total ' + str(count) + ' images be combined into the video at: ' + target_path + '\r\n')

imgs_path = 'result/kitti_tracking/'
seq = ['0020']
for s in seq:
    imgs_path_seq = imgs_path + s +'/out_ps/'
    imgs2video(imgs_path_seq,ps=False)