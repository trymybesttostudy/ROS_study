import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv


# 读取图片
def ReadImg():
    img = cv2.imread('img.png', 1)
    plt.imshow(img)
    return img


# 腐蚀运算
def erode(src):
    # 创建核结构
    kernel = np.ones((5, 5), np.uint8)
    # 图像腐蚀
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


# 轮廓拟合
def draw_shape(open_img, gray_img):
    contours, hierarchy = cv2.findContours(open_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]  # 得到第一个的轮廓

    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    src = ReadImg()
    cv2.drawContours(src, [box], -1, (0, 0, 255), 3)  # 画矩形框

    # 图像轮廓及中心点坐标
    M = cv2.moments(cnt)  # 计算第一条轮廓的各阶矩,字典形式
    center_x = int(M['m10'] / M['m00'])
    center_y = int(M['m01'] / M['m00'])
    print('center_x:', center_x)
    print('center_y:', center_y)
    cv2.circle(src, (center_x, center_y), 7, 128, -1)  # 绘制中心点
    str1 = '(' + str(center_x) + ',' + str(center_y) + ')'  # 把坐标转化为字符串
    cv2.putText(src, str1, (center_x - 50, center_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                cv2.LINE_AA)  # 绘制坐标点位


src = ReadImg()
gaus_img = GausBlur(src)
gray_img = Gray_img(gaus_img)
thres_img = threshold_img(gray_img)
open_img = open_mor(thres_img)
draw_shape(open_img, src)


###################################
#plt.subplot(1, 1, 1),    plt.imshow(src),                   plt.title('read')              # 轮廓点绘制的颜色通道是BGR; 但是Matplotlib是RGB;
plt.subplot(1, 4, 1),    plt.imshow(gray_img),              plt.title('gray_img')           # 故在绘图时，(0, 0, 255)会由BGR转换为RGB（红 - 蓝）
plt.subplot(1, 4, 2),    plt.imshow(thres_img),             plt.title('thres_img')
plt.subplot(1, 4, 3),    plt.imshow(open_img),              plt.title('open_img')
plt.subplot(1, 4, 4),    plt.imshow(src),                   plt.title('answer')
plt.show()

"""######################################################################
# （1）轮廓检测：contours, hierarchy = cv2.findContours(img, mode, method)
# 输入参数      mode: 轮廓检索模式
#                   （1）RETR_EXTERNAL：  只检索最外面的轮廓；
#                   （2）RETR_LIST：      检索所有的轮廓，但检测的轮廓不建立等级关系，将其保存到一条链表当中，
#                   （3）RETR_CCOMP：     检索所有的轮廓，并建立两个等级的轮廓。顶层是各部分的外部边界，内层是的边界信息;
#                   （4）RETR_TREE：      检索所有的轮廓，并建立一个等级树结构的轮廓;（最常用）
#               method: 轮廓逼近方法
#                   （1）CHAIN_APPROX_NONE：      存储所有的轮廓点，相邻的两个点的像素位置差不超过1。               例如：矩阵的四条边。（最常用）
#                   （2）CHAIN_APPROX_SIMPLE:     压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标。   例如：矩形的4个轮廓点。
# 输出参数      contours：所有的轮廓
#               hierarchy：每条轮廓对应的属性
# 备注0：轮廓就是将连续的点（连着边界）连在一起的曲线，具有相同的颜色或者灰度。轮廓在形状分析和物体的检测和识别中很有用。
# 备注1：函数输入图像是二值图，即黑白的（不是灰度图）。所以读取的图像要先转成灰度的，再转成二值图。
# 备注2：函数在opencv2只返回两个值：contours, hierarchy。
# 备注3：函数在opencv3会返回三个值：img, countours, hierarchy
######################################################################
# （2）绘制轮廓：v2.drawContours(image, contours, contourIdx, color, thickness) ———— (在图像上)画出图像的轮廓
# 输入参数        image:              需要绘制轮廓的目标图像，注意会改变原图
#                 contours:           轮廓点，上述函数cv2.findContours()的第一个返回值
#                 contourIdx:         轮廓的索引，表示绘制第几个轮廓。-1表示绘制所有的轮廓
#                 color:              绘制轮廓的颜色(RGB)
#                 thickness:          （可选参数）轮廓线的宽度，-1表示填充
# 备注：图像需要先复制一份copy(), 否则（赋值操作的图像）与原图会随之一起改变。
######################################################################
# （3）计算轮廓的长度：retval = cv2.arcLength(curve, closed)
# 输入参数：      curve              轮廓（曲线）。
#                 closed             若为true,表示轮廓是封闭的；若为false，则表示打开的。（布尔类型）
#
# 输出参数：      retval             轮廓的长度（周长）。
######################################################################
# （4）找出轮廓的多边形拟合曲线：approxCurve = approxPolyDP(contourMat, epsilon, closed);
# 输入参数：     contourMat：        轮廓点矩阵（集合）
#                epsilon：           (double类型)指定的精度, 即原始曲线与近似曲线之间的最大距离。
#                closed：            (bool类型)若为true, 则说明近似曲线是闭合的; 反之, 若为false, 则断开。
# 
# 输出参数：     approxCurve：       轮廓点矩阵（集合）；当前点集是能最小包容指定点集的。画出来即是一个多边形；
######################################################################
# （5）绘制矩形边框:cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#       (x, y)：         矩形定点
#       (x+w, y+h)：     矩形的宽高
#       (0,0,225)：      矩形的边框颜色；
#       2：              矩形边框宽度
######################################################################
# cv2.putText(image, text, (5,50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

位置参数说明：

        image = 图片
        text = 要添加的文字
        () = 文字添加到图片上的位置
        字体的类型
        字体大小
        字体颜色
        字体粗细
######################################################################

"""


