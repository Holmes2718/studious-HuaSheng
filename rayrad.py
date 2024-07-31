import cv2
import numpy as np

class ColorFinding:
cap = cv2.VideoCapture(0)

mycolors = [[153,105,132,175,255,255]]
mycolorvaules = [[51,153,255]]# rbg颜色  BGR
myPoints = []  #x,y,colorid 制作点的集合用于画线


def findColor(img,mycolor,mycolorvaule):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in mycolor:#展现三个窗口，每个窗口显示颜色不同
        #lower = np.array(mycolor[0][0:3])#行  列（[1,4））
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorvaule[count],cv2.FILLED)

        if x != 0 and y != 0:
            newPoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    x,y,w,h = 0,0,0,0
    _,contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#输入，只检测外轮廓，存储所有的轮廓点
    for cnt in contours:

        area = cv2.contourArea(cnt)#计算轮廓面积
        if area>500:#像素大于500才有效
            # cv2.drawContours(imgResult,cnt,-1,(255,0,0),2)#找到点之后可以注释掉
            peri = cv2.arcLength(cnt,True)#计算轮廓周长 后者为是否为封闭曲线
            appprox = cv2.approxPolyDP(cnt,0.02*peri,True)#保留重要顶点，删除多余顶点（找到多边形各角，其包含数据数量为角个数） 输入，精度，是否封闭
            x,y,w,h = cv2.boundingRect(appprox)#根据图形最大长和宽画出其近似轮廓的相关值 前：返回矩形边界左上角顶点的坐标值及矩形边界的宽和高
            cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(x+w//2,y+h//2)
    return x+w//2,y+h//2


def drawPoint(point,colorvaule):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,mycolorvaules[point[2]],cv2.FILLED)

# 视频

while True:
    success,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, mycolors,mycolorvaules)

    cv2.imshow("1", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break