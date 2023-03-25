import cv2
import requests
import numpy as np
import matplotlib.pyplot as plt

file = requests.get("https://files-cdn.cnblogs.com/files/shiwanghualuo/1.bmp")
img = cv2.imdecode(np.frombuffer(file.content, np.uint8), 1)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# opencv2 返回两个值：coutours,hierarchy
# opencv3 返回三个值：img, coutours, hierarchy
contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
rect = cv2.minAreaRect(contours[0]) # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
print(rect)
box = cv2.boxPoints(rect) # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
print(box)  #
box = np.intp(box)
# 画出来
cv2.drawContours(img, [box], 0, (0, 0, 255), 5)
# cv2.imwrite('contours.png', img)
plt.imshow(img)
plt.show()
# out
# rect: ((144.0, 154.0), (150.0, 170.0), -90.0)
# box:
# [[229. 229.]
# [ 59. 229.]
# [ 59.  79.]
# [229.  79.]]
