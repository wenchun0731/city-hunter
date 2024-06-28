import cv2
from PIL import Image
import glob
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

# 照片路径
# files = glob.glob('path/to/your/images/*.jpg')

def photo_resize(img, target_width, target_height):
    re_img = cv2.resize(img, (target_width, target_height))
    return re_img

def adjusted(img, x, y):
    alpha = x
    beta = y
    adjusted_image = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted_image

def Sobel(img):
    Sobelx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    Sobelx = cv2.convertScaleAbs(Sobelx)
    return Sobelx

def Gussian(img):
    kernel_size = (3, 3)
    sigma_x = 0
    blurred_img = cv2.GaussianBlur(img, kernel_size, sigma_x)
    return blurred_img

def threshold(img):
    thr, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return binary

def contours(img):
    contours1, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    letters = []
    for contour in contours1:
        x, y, w, h = cv2.boundingRect(contour)
        if 15 < h < 85:
            letters.append(contour)
    min_x = float('inf')
    max_x = 0
    for letter in letters:
        for point in letter:
            x = point[0][0]
            min_x = min(min_x, x)
            max_x = max(max_x, x)
    return min_x, max_x

def cropped(img, x, y, h, w):
    cropped_img = img[y:h, x:w]
    return cropped_img

def erope(img):
    kernel = np.ones((3, 3), np.uint8)
    ero = cv2.erode(img, kernel, iterations=1)
    return ero

def dilate(img):
    kernel = np.ones((2, 7), np.uint8)
    dilation = cv2.dilate(img, kernel, iterations=9)
    return dilation

def findcontour(img):
    contours1, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = None
    min_contour_length = 2500
    for contour in contours1:
        area = cv2.contourArea(contour)
        if area >= min_contour_length:
            rect = cv2.minAreaRect(contour)
            angle = rect[2]
            points = cv2.boxPoints(rect)
            points = np.int0(points)
            break
    if points is not None:
        if angle >= 0:
            sorted_points = sorted(points, key=lambda x: x[0])
            bottom_left, top_left, bottom_right, top_right = sorted_points[0], sorted_points[1], sorted_points[2], sorted_points[3]
        else:
            sorted_points = sorted(points, key=lambda x: x[0])
            top_left, bottom_left, top_right, bottom_right = sorted_points[0], sorted_points[1], sorted_points[2], sorted_points[3]
        return bottom_left, top_left, bottom_right, top_right
    else:
        return 0, 0, 0, 0

def affine(img, bottom_left, top_left, bottom_right, top_right):
    p1 = np.float32([top_left, top_right, bottom_right])
    p2 = np.float32([[top_left[0], top_right[1]], top_right, bottom_right])
    M = cv2.getAffineTransform(p1, p2)
    h, w = img.shape[:2]
    output = cv2.warpAffine(img, M, (w, h))
    x, y = 0, min(top_right[1], bottom_right[1])
    h = abs(bottom_right[1] - top_right[1])
    output = output[y-5:y+h, x:x+w]
    output = adjusted(output, -1.5, 15)
    if output is not None:
        cv2.imwrite('output.jpg', output)
    else:
        print('None')
        pass

def tesseracttt(img_path):
    config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. --oem 3 --psm 6'
    img = cv2.imread(img_path)
    text = pytesseract.image_to_string(img, lang='eng', config=config)
    if len(text.strip()) == 0:
        print('辨識失敗')
    else:
        clean_text = text.strip()
        # print('辨識結果:\n{}'.format(clean_text))
        # cv2.putText(img, clean_text, (110, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # plt.axis('off')
        # plt.show()
        return clean_text


