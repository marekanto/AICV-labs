import numpy as np
import cv2 as cv
from matplotlib import pyplot as plot
from skimage.util import random_noise


def gaussian_noise(img):
    m = 0
    dev_1 = 0.05
    dev_2 = 0.08
    var1 = dev_1 ** 2
    var2 = dev_2 ** 2
    # ret1 = random_noise(img, mode='gaussian', mean=m, var=var1,seed=None, clip=True)
    ret2 = random_noise(img, mode='gaussian', mean=m, var=var2, seed=None, clip=True)
    ret2 = (255 * ret2).astype(np.uint8)  # float-> int
    return ret2


def salt_pepper_filter(img):
    return_1 = random_noise(img, mode='s&p', seed=None, clip=True, amount=0.2)

    return_1 = (255 * return_1).astype(np.uint8)  # float-> int
    cv.imshow('s&p_noise', return_1)

    fil = cv.medianBlur(return_1, 3)
    cv.imshow('s&p_filtered', fil)
    return fil


def gaussian_filter(img):
    return_1 = cv.GaussianBlur(img, (3, 3), 0)
    return return_1


def sharpen(img, blur_img):
    return_1 = cv.addWeighted(img, 1.5, blur_img, -0.5, 0)
    cv.imshow('Final Picture', return_1)


def sobel(img):
    sobelx = cv.Sobel(img, cv.CV_8U, 1, 0, ksize=3)
    sobely = cv.Sobel(img, cv.CV_8U, 0, 1, ksize=3)

    plot.subplot(1, 2, 1), plot.imshow(sobelx, cmap='gray')
    plot.title('Sobel X')
    plot.subplot(1, 2, 2), plot.imshow(sobely, cmap='gray')
    plot.title('Sobel Y')
    plot.show()


def laplace(img, kernel):  # explaination in documenetation
    k_cols, k_rows = kernel.shape
    pad = (k_cols - 1) // 2
    rows, cols = img.shape
    length = rows + 2 * pad  # *2 because of left and right
    width = cols + 2 * pad  # *2 because of top and bottom
    img2 = np.zeros((length, width), dtype=np.uint8)
    for row in range(0, rows):
        img2[row, 0] = img[row, 0]
        img2[row, width - 1] = img[row, cols - 1]
        for col in range(0, cols):
            img2[row + 1, col + 1] = img[row, col]
            img2[0, col] = img[0, col]
            img2[length - 1, col] = img[rows - 1, col]

    return_1 = cv.filter2D(img2, -1, kernel)
    blurred = gaussian_filter(img)
    laplacian = cv.Laplacian(blurred, cv.CV_8U, ksize=5)
    cv.imshow('laplacian', laplacian)
    cv.imshow('Final Picture', return_1)


img = cv.imread('lena.png', cv.IMREAD_GRAYSCALE)
# cv.imshow('Original', img)

# noise_img = gaussian_noise(img)

# cv.imshow('Noise image', noise_img)
# blur_img = gaussian_filter(noise_img)
# cv.imshow('blur image', blur_img)
# sharpen(img, blur_img)

# blur_img=salt_pepper(img)
# sharpen(img,blur_img)
kernel = np.array((
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, -24, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]), dtype="int")

laplace(img, kernel)
# sobel(noise_img)
cv.waitKey()

cv.destroyAllWindows()
