import cv2
import matplotlib.pyplot as plt         # Matplotlib是RGB

###################################
# 图像二值化 ———— 图像轮廓检测的输入图像是二值图，即黑白的（不是灰度图）
img = cv2.imread("img.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                        # 灰度图
ret, thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)      # 二值化
###################################
# （1）图像轮廓检测
draw_img1 = img.copy()
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# 画出图像的轮廓(在图像上) —— 注意：图像需要copy(), 否则原图会随之一起改变。
res1 = cv2.drawContours(draw_img1, contours, -1, (0, 0, 255), 2)
###################################
# （2）轮廓的多边形拟合曲线
draw_img2 = img.copy()
contours1 = contours[0]
epsilon = 0.21*cv2.arcLength(contours1, True)       	# 系数k：越小越接近于真实轮廓，越大拟合越粗糙
approx = cv2.approxPolyDP(contours1, epsilon, True)
# 画出图像的轮廓(在图像上) —— 注意：图像需要copy(), 否则原图会随之一起改变。
res2 = cv2.drawContours(draw_img2, [approx], -1, (0, 0, 255), 2)
###################################
# （3）用矩形画出轮廓的边界
draw_img3 = img.copy()
x, y, w, h = cv2.boundingRect(contours1)
img_rectangle = cv2.rectangle(draw_img3, (x, y), (x+w, y+h), (0, 255, 0), 2)
###################################
# （4）用外接圆画出轮廓的边界
draw_img4 = img.copy()
(x, y), radius = cv2.minEnclosingCircle(contours1)
center = (int(x), int(y))
radius = int(radius)
img_circle = cv2.circle(draw_img4, center, radius, (0, 255, 0), 2)
###################################
#plt.subplot(1, 1, 1),    plt.imshow(img),               plt.title('RAW')           # 轮廓点绘制的颜色通道是BGR; 但是Matplotlib是RGB;
plt.subplot(1, 1, 1),    plt.imshow(res1),              plt.title('findContours')  # 故在绘图时，(0, 0, 255)会由BGR转换为RGB（红 - 蓝）
#plt.subplot(2, 3, 3),    plt.imshow(res2),              plt.title('approxPolyDP')
#plt.subplot(2, 3, 4),    plt.imshow(draw_img3),         plt.title('rectangle')
#plt.subplot(2, 3, 5),    plt.imshow(draw_img4),         plt.title('circle')
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
######################################################################"""

