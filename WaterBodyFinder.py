import cv2
import numpy as np
from random import randint
from sklearn.cluster import DBSCAN

'''
This is a program that finds the water bodies in a satellite image. It uses the DBSCAN algorithm to find the water
bodies, and outputs a new image with the oceans colored with (255, 100, 100), or "pink".
The hyperparameters and color matching function are tuned for an image with size 1000x1000. The images are downloaded
using HERE API, using the Image_Gen.py script.

Sample images provided: "map_world.png", "map_Europe.png"
'''

def is_water(r, g, b):
    if r < 50:  # this function seems to work well, based on tuning; could be improved
        return True
    return False

fn = "map_Europe.png" # map file name, can be changed
img = cv2.imread(fn, cv2.IMREAD_COLOR)
first_im = img.copy()
f_x = img.shape[0]
f_y = img.shape[1]
img = cv2.resize(img, (img.shape[0] // 5, img.shape[1] // 5)) # resize image so that it is faster to process
or_img = img.copy()
or_x, or_y = img.shape[0], img.shape[1]
img = img.reshape(-1, 3)

D = DBSCAN(eps=10, min_samples=40).fit(img)  # labels for each pixel
a = D.labels_.reshape(or_x, or_y) # reshape the labels to the original image size

img2 = []
colmap = {}


for ind_x, x in enumerate(a):
    arr = []
    for ind_y, y in enumerate(x):
        if y not in colmap:
            colmap[y] = [randint(0, 255), randint(0, 255), randint(0, 255)] if is_water(or_img[ind_x][ind_y][2], or_img[ind_x][ind_y][1], or_img[ind_x][ind_y][0]) else [0, 0, 0]
        if y != -1:
            arr.append(colmap[y])
        else:
            arr.append([0, 0, 0])
    img2.append(arr)
final_img = np.array(img2).reshape(or_x, or_y, 3)
final_img = cv2.resize(final_img, (f_x, f_y), interpolation=cv2.INTER_NEAREST)


for i in range(first_im.shape[0]):
    for j in range(first_im.shape[1]):
        if final_img[i][j][0] == 0 and final_img[i][j][1] == 0 and final_img[i][j][2] == 0:
            for k in range(3):
                final_img[i][j][k] += first_im[i][j][k]
        else:
            final_img[i][j][0] = 100
            final_img[i][j][1] = 100
            final_img[i][j][2] = 255

cv2.imwrite(fn[:-4]+"_clustered.png", final_img)


