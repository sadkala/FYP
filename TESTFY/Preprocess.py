# Preprocess.py

import cv2
import numpy as np
import math

# module level variables ##########################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)       #高斯模糊x和y的大小
ADAPTIVE_THRESH_BLOCK_SIZE = 21 ##19is original value ###still repairing ###27 is good
ADAPTIVE_THRESH_WEIGHT = 3 ## 3repair=O,U,R|||13repiar=8,6  originalvalue =9

###################################################################################################
def preprocess(imgOriginal):
    imgGrayscale = extractValue(imgOriginal)        ##HSV的V image

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)     ##(原圖+開運算)-閉運算 的圖

    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)       #create grey image

    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)  ##高斯模糊

    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)####tresh值有需要修改

    return imgGrayscale, imgThresh
# end function

###################################################################################################
def extractValue(imgOriginal):
    height, width, numChannels = imgOriginal.shape      ##picture shape

    imgHSV = np.zeros((height, width, 3), np.uint8)     ##create a black image

    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)   ##BGR change HSV night space ##opencv default color is BGR

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)     ##split image channel HSV(H爲0到360，S爲0到1，V爲0到255。) 

    return imgValue       ##return V
# end function

###################################################################################################
def maximizeContrast(imgGrayscale):                     ##red and original image

    height, width = imgGrayscale.shape                 ##image shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)        ##grey image
    imgBlackHat = np.zeros((height, width, 1), np.uint8)      #grey image

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))    ##定义矩形         ####闭运算用来连接被误分为许多小块的对象，而开运算用于移除由图像噪音形成的斑点

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement) #原圖-開運算（侵蝕在膨脹
    
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)#原圖-閉運算（膨脹在侵蝕

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)           ##red and original image and 開運算image merge together
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)  ##then subtract with 閉運算image

    return imgGrayscalePlusTopHatMinusBlackHat
# end function










