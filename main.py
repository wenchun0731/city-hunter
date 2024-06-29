from platesID import photo_resize,adjusted,Sobel,Gussian,bg,threshold,contours,cropped,erope,dilate,findcontour,affine,tesseracttt
from connectDB import connect,creatdata,com
import cv2


image=cv2.imread('IMG_7434.JPG')
img=image
#尺寸調整
img = photo_resize(img, 300, 136)
#對比度與亮度
adj_img = adjusted(img, -1.5, 15)
#灰階
gray_img = cv2.cvtColor(adj_img, cv2.COLOR_BGR2GRAY)
#Sobel
Sobelx = Sobel(gray_img)
#高斯模糊
blur_img = Gussian(Sobelx)
#二值化
binary = threshold(blur_img)
#找出輪廓
min_x, max_x = contours(binary)
#裁切
cropped_img = cropped(binary, min_x, 0, binary.shape[0], max_x)
#侵蝕
ero_img = erope(cropped_img)
#膨脹
dilate_img = dilate(ero_img)
#最小矩形
bottom_left, top_left, bottom_right, top_right = findcontour(dilate_img)
#裁切
adj_img = cropped(adj_img, min_x, 0, img.shape[0], max_x)
#訪設變換
affine(adj_img, bottom_left, top_left, bottom_right, top_right)
#加背景
bg('output.jpg')
#字元辨識
text=tesseracttt('output.jpg')
print('Hello')

cnx,cursor=connect()
creatdata(text,cursor)
com(cnx)
print(text)