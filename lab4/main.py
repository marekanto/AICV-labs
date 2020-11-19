import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt #importing matplotlib
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def quantize_img(img,intensity):
    adjusted_int = 256/intensity
    adjusted_int = int(adjusted_int)
    img2 = img.copy()
    rows,cols = img.shape[:2]
    contrast = img.std()
    for row in range(0,rows):
        for col in range(0,cols):
            index = img2[row,col] / adjusted_int
            index_after_quant = int(index) * adjusted_int
            img2[row, col] = int(index_after_quant)
            # if (col % adjusted_int) != 0:
            #     img2[row,col] = index
            # else:
            #     index = img2[row,col]
    return img2

def stretch_img(img):
    rows, cols = img.shape[:2]
    img2 = img.copy()
    max = np.max(img2)
    min = np.min(img2)
    for row in range (0,rows):
        for col in range(0,cols):
                img2[row,col] = (((img2[row,col] - min)/(max - min) ) * 255)

    return img2

def resize(img):
    src = img.copy()
    scale_percent = 50  # percent of original size
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(src, dim, interpolation=cv.INTER_AREA)
    return resized



def equalize_histogram(img):

    equ = cv.equalizeHist(img)
    res = np.hstack((img, equ))  # stacking images side-by-side
    cv.imshow('Compareing Before and after Equalization', res)
    return res

img1 = cv.imread('lena.png',0)
img = resize(img1)
img_high = cv.imread('landscape.jpg',0)
img128 = quantize_img(img,128)
img64 = quantize_img(img,64)
img32 = quantize_img(img,32)

img64_s = stretch_img(img64)
img32_s = stretch_img(img32)
# img32_e = equalize_histogram(img32)

histg = cv.calcHist([img],[0],None,[256],[0,256])
histg32 = cv.calcHist([img32_s],[0],None,[256],[0,256])
histg64 = cv.calcHist([img64],[0],None,[256],[0,256])
histg128 = cv.calcHist([img128],[0],None,[256],[0,256])
histg32_e = cv.calcHist([img32_s],[0],None,[256],[0,256])

# plt.plot(histg)
# # plt.show()
# plt.plot(histg32_e)
# plt.show()

# cv.imshow('original',img)
 # cv.imshow('quantized 128',img128)
# cv.imshow('quantized 64',img64)
# cv.imshow('stretched 64',img64_s)
# cv.imshow('quantized 32',img32)
# cv.imshow('stretched 32', img32_s)

cv.waitKey(0)

dft = cv.dft(np.float32(img),flags = cv.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

rows, cols = img.shape
crow,ccol = int(rows/2) , int(cols/2)
# create a mask first, center square is 1, remaining all zeros
mask = np.zeros((rows,cols,2),np.uint8)
mask[crow-30:crow+30, ccol-30:ccol+30] = 1
# apply mask and inverse DFT


fshift = dft_shift*mask
f_ishift = np.fft.ifftshift(fshift)
img_back = cv.idft(f_ishift)
img_back = cv.magnitude(img_back[:,:,0],img_back[:,:,1])
plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img_back, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
