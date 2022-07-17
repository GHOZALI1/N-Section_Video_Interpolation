import cv2
import numpy as np,sys

A = cv2.imread('./frame2.jpg')
B = cv2.imread('./frame2.jpg')

# With the code above we read the images that we are going to use.

# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv2.pyrDown(gpA[i])
    gpA.append(G)

# Then we generate the Gaussian pyramid for the image with the apple.

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in range(6):
    G = cv2.pyrDown(gpB[i])
    gpB.append(G)

# We generate a Gaussian pyramid for the image with the orange.

# generate Laplacian Pyramid for A

lpA = [gpA[5]]
for i in range(5,0,-1):
    size = (gpA[i-1].shape[1], gpA[i-1].shape[0])
    GE = cv2.pyrUp(gpA[i], dstsize = size)
    L = cv2.subtract(gpA[i-1],GE)
    lpA.append(L)

# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in range(5,0,-1):
    size = (gpB[i-1].shape[1], gpB[i-1].shape[0])
    GE = cv2.pyrUp(gpB[i], dstsize = size)
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)

# We generate a Laplacian pyramid for both of the images.

# Now add left and right halves of images in each level
LS = []
for la,lb in zip(lpA,lpB):
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:int(cols/2)], lb[:,int(cols/2):]))
    LS.append(ls)

# We add the halves of the images.
# now reconstruct
ls_ = LS[0]
for i in range(1,6):
    size = (LS[i].shape[1], LS[i].shape[0])
    ls_ = cv2.pyrUp(ls_, dstsize = size)
    ls_ = cv2.add(ls_, LS[i])
cv2.imshow('RESULT',ls_)
cv2.imwrite('./Blend.jpg',ls_)
cv2.waitKey(0)