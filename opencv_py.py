#!/usr/bin/env python
# coding:utf-8

import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import matplotlib.pyplot as plt
import random
import cv2 as cv
from opencv_cam.msg import picture


global center_x_all_02, center_y_all_02, res, center_x_all_01, center_y_all_01, posture, sum, i, bridge
center_x_all_02 = []
center_x_all_01 = []
center_y_all_02 = []
center_y_all_01 = []
posture = []
center_all = []
center_all_L = []


def callback(data):

    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    cv2.imshow("frame" , cv_img)
    cv2.waitKey(10000)
    cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
    # 读入图像
    srcImage = cv_img

    # 腐蚀运算
    def erode(src):
        # 创建核结构
        kernel = np.ones((5, 5), np.uint8)
        # 图像腐蚀 g
        erosion = cv.erode(src, kernel)
        return erosion


    # 膨胀运算
    def dilate(src):
        # 创建核结构
        kernel = np.ones((5, 5), np.uint8)
        # 图像腐蚀
        dilate = cv.dilate(src, kernel)
        return dilate


    # 高斯滤波
    def GausBlur(src):
        dst = cv2.GaussianBlur(src, (5, 5), 1.5)
        plt.imshow(dst)
        return dst


    # 灰度处理
    def Gray_img(src):
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        return gray


    # 二值化
    def threshold_img(src):
        ret, binary = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
        print("threshold value %s" % ret)
        return binary


    # 开运算操作
    def open_mor(src):
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel, iterations=3)  # iterations进行3次操作
        return opening


    # 颜色识别——01
    def ColorFindContours(srcImage, iLowH, iHighH, iLowS, iHighS, iLowV, iHighV):
        # 转为HSV
        imgHSV = cv2.cvtColor(srcImage, cv2.COLOR_BGR2HSV)
        bufImg = cv2.inRange(imgHSV, np.array((iLowH, iLowS, iLowV)), np.array((iHighH, iHighS, iHighV)))
        return bufImg


    # 颜色识别——02
    def ColorFindContours2(srcImage):
        des1 = ColorFindContours(srcImage,
            350 / 2, 360 / 2,        # 色调最小值~最大值
            (int)(255 * 0.70), 255,  # 饱和度最小值~最大值
            (int)(255 * 0.60), 255)  # 亮度最小值~最大值

        des2 = ColorFindContours(srcImage,
            0, (int)(16 / 2),        # 色调最小值~最大值
            (int)(255 * 0.70), 255,  # 饱和度最小值~最大值
            (int)(255 * 0.60), 255)  # 亮度最小值~最大值

        return des1 + des2


    # 膨胀操作
    def Dilate(src):
        # 创建核结构
        kernel = np.ones((5, 5), np.uint8)
        # 图像膨胀
        dilate = cv.dilate(src, kernel)
        return dilate


    # 腐蚀操作
    def Erode(src):
        # 创建核结构
        kernel = np.ones((5, 5), np.uint8)
        #图像腐蚀
        erode = cv.erode(src, kernel)
        return erode


    # 非 L 型方块轮廓拟合
    def draw_shape(open_img):
        # （1）图像轮廓检测
        i = 0
        draw_img = open_img.copy()
        contours, hierarchy = cv2.findContours(open_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.intp(box)
        # src = ReadImg()
        # cv2.drawContours(src, [box], -1, (0, 0, 255), 3)  # 画矩形框

        for cnt in contours:
            # 轮廓绘制
            # 画出图像的轮廓(在图像上) —— 注意：图像需要copy(), 否则原图会随之一起改变。
            res = cv2.drawContours(draw_img, cnt, 0, (0, 0, 0), -1)
            # 图像轮廓及中心点坐标
            M1 = cv2.moments(cnt)  # 计算第一条轮廓的各阶矩,字典形式
            # print(M1['m00'])
            # print(M1['m10'])
            center_x = float(M1['m10'] / M1['m00'])
            center_y = float(M1['m01'] / M1['m00'])

            print('center_x:', center_x)
            print('center_y:', center_y)
            center_x_all_01.append(center_x)
            center_y_all_01.append(center_y)
            center_all.append([center_x_all_01,center_y_all_01])

        return center_all


    # L 型方块轮廓拟合
    def draw_shape_L(open_img):

        # （1）图像轮廓检测
        s = 0
        draw_img = open_img.copy()
        contours, hierarchy = cv2.findContours(open_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            center = cv2.minAreaRect(cnt)[0]
            center_x = float(center[0])
            center_y = float(center[1])

            # 轮廓绘制
            # 画出图像的轮廓(在图像上) —— 注意：图像需要copy(), 否则原图会随之一起改变。
            res = cv2.drawContours(draw_img, contours[0], 0, (0, 0, 0), -1)
            # 图像轮廓及中心点坐标
            M1 = cv2.moments(cnt)  # 计算第一条轮廓的各阶矩,字典形式
            # print(M1['m00'])
            # print(M1['m10'])
            center_x_01 = float(M1['m10'] / M1['m00'])
            center_y_01 = float(M1['m01'] / M1['m00'])
            center_x_01 = center_x_01 - (center_x - center_x_01)
            center_y_01 = center_y_01 - 3 * (center_y - center_y_01)
            print('center_x_02:', center_x_01)
            print('center_y_02:', center_y_01)
            center_x_all_02.append(center_x_01)
            center_y_all_02.append(center_y_01)
            center_all_L.append([center_x_all_02,center_y_all_02])
        return center_all_L


    # 红色 I 型，橙色正方形 矩形图片角度检测
    def angle_picture_red(picture):
        sum = 0
        i = 1
        image, contours = cv2.findContours(picture, 2, 4)

        # img = img.astype(np.float32)

        for cnt in image:

            # print(cnt)
            # 最小外界矩形的宽度和高度
            width, height = cv2.minAreaRect(cnt)[1]
            print(width, height)
            if width * height > 100:
                # 最小的外接矩形
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
                box = np.float(box)
                if 0 not in box.ravel():

                    '''绘制最小外界矩形
                    for i in range(4):
                        cv2.line(image, tuple(box[i]), tuple(box[(i+1)%4]), 0)  # 5
                    '''
                    # 旋转角度
                    theta = cv2.minAreaRect(cnt)[2]
                    if abs(theta) <= 90:
                        if width > height:
                            theta += -90
                        print(i, '图片的旋转角度为%s.' % theta)
                        posture.append(theta)
                        sum += 1
                        i += 1
                # print(posture[sum-1])
                # print(box)
        return posture


    # 黄色，紫色 L 型方块 图片角度检测
    def angle_picture_yellow_purple(picture):

        sum = 0
        i = 1
        image, contours = cv2.findContours(picture, 2, 4)

        # img = img.astype(np.float32)

        for cnt in image:
            M = cv2.moments(cnt)  # 计算第二条轮廓的各阶矩,字典形式
            center_x = float(M['m10'] / M['m00'])
            center_y = float(M['m01'] / M['m00'])
            # print(cnt)
            # 最小外界矩形的宽度和高度
            width, height = cv2.minAreaRect(cnt)[1]
            print(width, height)
            if width * height > 100:
                # 最小的外接矩形
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
                box = np.floatp(box)
                if 0 not in box.ravel():

                    '''绘制最小外界矩形
                    for i in range(4):
                        cv2.line(image, tuple(box[i]), tuple(box[(i+1)%4]), 0)  # 5
                    '''
                    # 旋转角度
                    theta = cv2.minAreaRect(cnt)[2]
                    center = cv2.minAreaRect(cnt)[0]
                    if abs(theta) <= 90:
                        if width > height:
                            theta += -90
                        if center[0] < center_x:
                            theta += 180
                        print(i, '图片的旋转角度为%s.' % theta)
                        posture.append(theta)
                        sum += 1
                        i += 1
                # print(posture[sum-1])
                # print(box)

        return posture


    # 绿色，蓝色 Z 字型方块 图片角度检测
    def angle_picture_green_blue(picture):

        sum = 0
        i = 1
        image, contours = cv2.findContours(picture, 2, 4)

        # img = img.astype(np.float32)

        for cnt in image:

            # print(cnt)
            # 最小外界矩形的宽度和高度
            width, height = cv2.minAreaRect(cnt)[1]
            print(width, height)
            if width * height > 100:
                # 最小的外接矩形
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
                box = np.floatp(box)
                if 0 not in box.ravel():

                    '''绘制最小外界矩形
                    for i in range(4):
                        cv2.line(image, tuple(box[i]), tuple(box[(i+1)%4]), 0)  # 5
                    '''
                    # 旋转角度
                    theta = cv2.minAreaRect(cnt)[2]
                    if abs(theta) <= 90:
                        if width > height:
                            theta += -90
                        print(i, '图片的旋转角度为%s.' % theta)
                        posture.append(theta)
                        sum += 1
                        i += 1
                # print(posture[sum-1])
                # print(box)
        return posture


    #  棕色山字型方块 图片角度检测
    def angle_picture_brown(picture):

        sum = 0
        i = 1
        image, contours = cv2.findContours(picture, 2, 4)

        # img = img.astype(np.float32)

        for cnt in image:
            M = cv2.moments(cnt)  # 计算第二条轮廓的各阶矩,字典形式
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])
            # print(cnt)
            # 最小外界矩形的宽度和高度
            width, height = cv2.minAreaRect(cnt)[1]
            print(width, height)
            if width * height > 100:
                # 最小的外接矩形
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
                box = np.floatp(box)
                if 0 not in box.ravel():

                    '''绘制最小外界矩形
                    for i in range(4):
                        cv2.line(image, tuple(box[i]), tuple(box[(i+1)%4]), 0)  # 5
                    '''
                    # 旋转角度
                    theta = cv2.minAreaRect(cnt)[2]
                    center = cv2.minAreaRect(cnt)[0]
                    if abs(theta) <= 90:
                        if width > height:
                            theta += -90
                        if center[0] > center_x:
                            theta += 180
                            print(center[1])
                        print(i, '图片的旋转角度为%s.' % theta)
                        posture.append(theta)
                        sum += 1
                        i += 1
                # print(posture[sum-1])
                # print(box)

        return posture

    # 橙色正方型方块 图片角度检测
    def angle_picture_orange(picture):

        sum = 0
        i = 1
        image, contours = cv2.findContours(picture, 2, 4)

        # img = img.astype(np.float32)

        for cnt in image:

            # print(cnt)
            # 最小外界矩形的宽度和高度
            width, height = cv2.minAreaRect(cnt)[1]
            print(width, height)
            if width * height > 100:
                # 最小的外接矩形
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点
                box = np.floattp(box)
                if 0 not in box.ravel():

                    '''绘制最小外界矩形
                    for i in range(4):
                        cv2.line(image, tuple(box[i]), tuple(box[(i+1)%4]), 0)  # 5
                    '''
                    # 旋转角度
                    theta = cv2.minAreaRect(cnt)[2]
                    if abs(theta) <= 90:
                        print(i, '图片的旋转角度为%s.' % theta)
                        posture.append(theta)
                        sum += 1
                        i += 1
                # print(posture[sum-1])
                # print(box)
        return posture



    # srcImage = cv_img


    # 根据颜色提取图像
    "--------------- 红色I型方块--------------- "
    des_red = ColorFindContours(srcImage,
        350 / 2, 359 / 2,           # 色调最小值~最大值
        (int)(255 * 0.60), 255 * 0.93,   # 饱和度最小值~最大值
        (int)(255 * 0.25), 255 * 0.35)  # 亮度最小值~最大值

    des_red = Dilate(des_red)
    des_red = Erode(des_red)
    des_red = Erode(des_red)
    des_red = Dilate(des_red)
    des_red = Dilate(des_red)
    des_red = Dilate(des_red)
    des_red = Dilate(des_red)

    "--------------- 紫色L型右方块--------------- "
    des_purple = ColorFindContours(srcImage,
        45 / 2, 60 / 2,           # 色调最小值~最大值
        (int)(255 * 0.60), 255,   # 饱和度最小值~最大值
        (int)(255 * 0.90), 255)  # 亮度最小值~最大值


    "--------------- 黄色L型左方块--------------- "
    des_yellow = ColorFindContours(srcImage,
        43 / 2, 64 / 2,           # 色调最小值~最大值
        (int)(255 * 0.65), 255,   # 饱和度最小值~最大值
        (int)(255 * 0.27), 255 * 0.51)  # 亮度最小值~最大值
    des_yellow = Dilate(des_yellow)
    des_yellow = Dilate(des_yellow)


    "--------------- 蓝色Z型左方块--------------- "
    des_blue = ColorFindContours(srcImage,
        45 / 2, 60 / 2,           # 色调最小值~最大值
        (int)(255 * 0.36), 255 * 0.51,   # 饱和度最小值~最大值
        (int)(255 * 0.14), 255 * 0.20)  # 亮度最小值~最大值


    "--------------- 绿色Z型右方块--------------- "
    des_green = ColorFindContours(srcImage,
        132 / 2, 172 / 2,           # 色调最小值~最大值
        (int)(255 * 0.24), 255 * 0.70,   # 饱和度最小值~最大值
        (int)(255 * 0.09), 255 * 0.20)  # 亮度最小值~最大值
    des_green = Erode(des_green)
    des_green = Dilate(des_green)
    des_green = Dilate(des_green)


    "--------------- 橙色田字型方块--------------- "
    des_orange = ColorFindContours(srcImage,
        2 / 2, 12 / 2,           # 色调最小值~最大值
        (int)(255 * 0.60), 255 * 0.98,   # 饱和度最小值~最大值
        (int)(255 * 0.34), 255 * 0.47)  # 亮度最小值~最大值
    des_orange = Dilate(des_orange)


    "--------------- 棕色山字型方块--------------- "
    des_brown = ColorFindContours(srcImage,
        7 / 2, 60 / 2,           # 色调最小值~最大值
        (int)(255 * 0.23), 255 * 0.68,   # 饱和度最小值~最大值
        (int)(255 * 0.10), 255 * 0.22)  # 亮度最小值~最大值
    des_brown = Erode(des_brown)
    des_brown = Dilate(des_brown)
    des_brown = Dilate(des_brown)



    "--------------- 图像旋转角度检测 --------------- "
    angle_red = angle_picture_red(des_red)
    angle_brown = angle_picture_brown(des_brown)
    angle_orange = angle_picture_orange(des_orange)
    angle_blue = angle_picture_green_blue(des_blue)
    angle_green = angle_picture_green_blue(des_green)
    angle_purple = angle_picture_yellow_purple(des_purple)
    angle_yellow = angle_picture_yellow_purple(des_yellow)


    "--------------- 轮廓坐标及角度 --------------- "


    picture.red.append([draw_shape(des_red),angle_red])
    picture.brown.append([draw_shape(des_brown),angle_brown])
    picture.orange.append([draw_shape(des_orange),angle_orange])
    picture.blue.append([draw_shape(des_blue),angle_blue])
    picture.green.append([draw_shape(des_green),angle_green])
    picture.purple.append([draw_shape(des_purple),angle_purple])
    picture.yellow.append([draw_shape(des_yellow),angle_yellow])
    

if __name__ == '__main__':
    rospy.init_node('sub_opencv', anonymous=True)
    bridge = CvBridge()
    P = picture()
    P.red = []
    P.brown = []
    P.orange = []
    P.blue = []
    P.green = []
    P.purple = []
    P.yellow = []
    rospy.Subscriber('camera/image', Image, callback)

    pub_red = rospy.Publisher("red",float, queue_size=5)
    pub_brown = rospy.Publisher("brown",float, queue_size=5)
    pub_orange = rospy.Publisher("orange",float, queue_size=5)
    pub_blue = rospy.Publisher("blue",float, queue_size=5)
    pub_green = rospy.Publisher("green",float, queue_size=5)
    pub_purple = rospy.Publisher("purple",float, queue_size=5)
    pub_yellow = rospy.Publisher("yellow",float, queue_size=5)
    rate = rospy.Rate(10000)
    while not rospy.is_shutdown():
        pub_red.publish(picture.red)
        pub_brown.publish(picture.brown)
        pub_orange.publish(picture.orange)
        pub_blue.publish(picture.blue)
        pub_green.publish(picture.green)
        pub_purple.publish(picture.purple)
        pub_yellow.publish(picture.yellow)
    
    rospy.spin()
