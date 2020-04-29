import cv2 as cv


def main():
    # 读入图像
    src = cv.imread("../../data/cuted.png")
    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", src)

    # 形态学梯度 - 基本梯度
    se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3), (-1, -1))
    basic = cv.morphologyEx(src, cv.MORPH_GRADIENT, se)
    cv.imshow("basic gradient", basic)

    # 图像灰度化
    gray = cv.cvtColor(basic, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary", binary)


    se = cv.getStructuringElement(cv.MORPH_RECT, (1, 5), (-1, -1))
    binary = cv.morphologyEx(binary, cv.MORPH_DILATE, se)
    # 寻找轮廓
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 画矩形
    for c in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[c])
        area = cv.contourArea(contours[c])
        # 去除一些干扰矩形
        if area < 200:
            continue
        if h > (3*w) or h < 20:
            continue
        cv.rectangle(src, (x, y), (x+w, y+h), (0, 0, 255), 2, 8, 0)

    cv.imshow("result", src)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
    # 以下代码为调试代码
    print(__name__)