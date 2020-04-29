import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def custom_hist_row(gray):
    # 水平投影
    h, w = gray.shape
    hist = np.zeros([h], dtype=np.int32)

    # 统计每一行的黑点数
    for row in range(h):
        for col in range(w):
            pv = gray[row, col]
            print(pv)
            if pv >= 100:
                hist[row] += 1

    # pyplot 展示hist 图
    # y_pos = np.arange(0, h, 1, dtype=np.int32)
    # plt.bar(y_pos, hist, align='center', color='r', alpha=0.5)
    # plt.xticks(y_pos, y_pos)
    # plt.ylabel('Frequency')
    # plt.title('Histogram row')

    # # plt.plot(hist, color='r')
    # # plt.xlim([0, h])
    # plt.show()
    return hist


def custom_hist_column(gray):
    # 垂直投影
    h, w = gray.shape
    hist = np.zeros([w], dtype=np.int32)
    # 统计每一列的黑点数
    for row in range(h):
        for col in range(w):
            pv = gray[row, col]
            if pv >= 100:
                hist[col] += 1

    # pyplot 展示hist 图
    # y_pos = np.arange(0, w, 1, dtype=np.int32)
    # plt.bar(y_pos, hist, align='center', color='r', alpha=0.5)
    # plt.xticks(y_pos, y_pos)
    # plt.ylabel('Frequency')
    # plt.title('Histogram column')
    #
    # # plt.plot(hist, color='r')
    # # plt.xlim([0, w])
    # plt.show()
    return hist


def image_hist(image):
    cv.imshow("input", image)
    color = ('blue', 'green', 'red')
    for i, color in enumerate(color):
        hist = cv.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.show()


def get_reactangle(src, r_hist, c_hist):
    # (x,y) 起点；（x2，y2）终点
    x1 = y1 = x2 = y2 = 0
    h, w = src.shape
    r_std = np.max(r_hist)/3
    c_std = np.max(c_hist)/3
    for row in range(h-1):
        if r_hist[row] >= r_std:
            r_hist[row] = 1
        else:
            r_hist[row] = 0
        if row >= 1:
            if r_hist[row - 1] > r_hist[row]:
                y1 = row
            if r_hist[row - 1] < r_hist[row]:
                y2 = row

    for col in range(w):
        if c_hist[col] >= c_std:
            c_hist[col]=1
        else:
            c_hist[col]=0
        if col >= 1 :
            if c_hist[col-1] > c_hist[col]:
                x1 = col
            if c_hist[col-1] < c_hist[col]:
                x2 = col
    x = x1
    y = y1
    h = y2 - y1
    w = x2 - x1
    return x, y, h, w


def main():
    print('this message is from main function')
    # 读入图像
    src = cv.imread("../../data/test.png")
    # 创建窗口
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    # 图像灰度化
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 展示图像
    cv.imshow("input", gray)

    #
    # # 将图片二值化
    # retval, img = cv.threshold(src, 127, 255, cv.THRESH_BINARY_INV)
    # # kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # # img = cv.erode(img, kernel)
    # # cv.imshow('binary',cv.resize(img, None, fx=0.3, fy=0.3, interpolation=cv.INTER_AREA))
    # cv.imshow('binary', img)

    # 运行函数
    r_hist = custom_hist_row(gray)
    c_hist = custom_hist_column(gray)
    # image_hist(src)

    # 获取矩形位置
    x, y, h, w = get_reactangle(gray, r_hist, c_hist)

    # 画出矩形
    '''
    def rectangle(img: Any,
              pt1: Any,
              pt2: Any,
              color: Any,
              thickness: Any = None,
              lineType: Any = None,
              shift: Any = None) -> None
    '''
    cv.rectangle(src, (x, y), (h, w), (0, 0, 255), 2)
    cv.imshow("rectangle", src)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
    # 以下代码为调试代码
    print(__name__)
