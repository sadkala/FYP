# PossibleChar.py

import cv2
import numpy as np
import math

###################################################################################################
class PossibleChar:

    # constructor #################################################################################
    def __init__(self, _contour):
        self.contour = _contour

        self.boundingRect = cv2.boundingRect(self.contour)  ##用一个最小的矩形，把找到的形状包起来

        [intX, intY, intWidth, intHeight] = self.boundingRect ##

        self.intBoundingRectX = intX
        self.intBoundingRectY = intY
        self.intBoundingRectWidth = intWidth
        self.intBoundingRectHeight = intHeight

        self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight #面積

        self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2 #找出X軸的中心點
        self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2 #找出Y軸的中心點

        self.fltDiagonalSize = math.sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2)) #彼氏定理

        self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight) #比例
    # end constructor

# end class








