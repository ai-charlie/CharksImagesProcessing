# Python+OpenCV竖版古籍文字分割
# https://www.cnblogs.com/SaltyFishQF/p/11474482.html?tdsourcetag=s_pctim_aiomsg
import cv2
import numpy as np

HIOG = 50
VIOG = 3
Position = []

'''水平投影'''


def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    # 获取图像大小
    (h, w) = image.shape
    # 统计像素个数
    h_ = [0] * h
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    cv2.imshow('hProjection2',cv2.resize(hProjection, None, fx=0.3, fy=0.5, interpolation=cv2.INTER_AREA))
    cv2.waitKey(0)
    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8);
    (h, w) = image.shape
    w_ = [0] * w
    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1
    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255
    cv2.imshow('vProjection',cv2.resize(vProjection, None, fx=1, fy=0.1, interpolation=cv2.INTER_AREA))
    cv2.waitKey(0)
    return w_


def scan(vProjection, iog, pos=0):
    start = 0
    V_start = []
    V_end = []

    for i in range(len(vProjection)):
        if vProjection[i] > iog and start == 0:
            V_start.append(i)
            start = 1
        if vProjection[i] <= iog and start == 1:
            if i - V_start[-1] < pos:
                continue
            V_end.append(i)
            start = 0
    return V_start, V_end


def checkSingle(image):
    h = getHProjection(image)
    start = 0
    end = 0

    for i in range(h):
        pass


if __name__ == "__main__":
    # 读入原始图像
    origineImage = cv2.imread('../../data/test.png')
    # 图像灰度化
    # image = cv2.imread('test.jpg',0)
    image = cv2.cvtColor(origineImage, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('gray',image)
    # 将图片二值化
    retval, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # img = cv2.erode(img, kernel)
    # cv2.imshow('binary',cv2.resize(img, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA))
    # 图像高与宽
    (h, w) = img.shape
    # 垂直投影
    V = getVProjection(img)

    start = 0
    V_start = []
    V_end = []

    # 对垂直投影水平分割
    V_start, V_end = scan(V, HIOG)
    if len(V_start) > len(V_end):
        V_end.append(w - 5)

    # 分割行，分割之后再进行列分割并保存分割位置
    for i in range(len(V_end)):
        # 获取行图像
        if V_end[i] - V_start[i] < 30:
            continue

        cropImg = img[0:h, V_start[i]:V_end[i]]
        # cv2.imshow('cropImg',cropImg)
        # cv2.waitKey(0)
        # 对行图像进行垂直投影
        H = getHProjection(cropImg)
        H_start, H_end = scan(H, VIOG, 40)

        if len(H_start) > len(H_end):
            H_end.append(h - 5)

        for pos in range(len(H_start)):
            # 再进行一次列扫描
            DcropImg = cropImg[H_start[pos]:H_end[pos], 0:w]
            d_h, d_w = DcropImg.shape
            # cv2.imshow("dcrop", DcropImg)
            sec_V = getVProjection(DcropImg)
            c1, c2 = scan(sec_V, 0)
            if len(c1) > len(c2):
                c2.append(d_w)

            x = 1
            while x < len(c1):
                if c1[x] - c2[x - 1] < 12:
                    c2.pop(x - 1)
                    c1.pop(x)
                    x -= 1
                x += 1

            # cv2.waitKey(0)
            if len(c1) == 1:
                Position.append([V_start[i], H_start[pos], V_end[i], H_end[pos]])
            else:
                for x in range(len(c1)):
                    Position.append([V_start[i] + c1[x], H_start[pos], V_start[i] + c2[x], H_end[pos]])

    # 根据确定的位置分割字符
    for m in range(len(Position)):
        cv2.rectangle(origineImage, (Position[m][0] - 5, Position[m][1] - 5), (Position[m][2] + 5, Position[m][3] + 5),
                      (0, 0, 255), 2)
    cv2.imshow('image', cv2.resize(origineImage, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA))
    cv2.waitKey(0)