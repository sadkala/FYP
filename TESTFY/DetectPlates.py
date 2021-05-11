# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar

# module level variables ##########################################################################
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

###################################################################################################ok
def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginalScene.shape                   ###picture height,picture width,picture channel

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)           #create grey image
    imgThreshScene = np.zeros((height, width, 1), np.uint8)              #create grey image
    imgContours = np.zeros((height, width, 3), np.uint8)                 #create a black brg image

    cv2.destroyAllWindows()

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("0", imgOriginalScene)
    # end if # show steps #########################################################################

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images ##going to Preprocess.py ###return (red and originalimage) and (gaussian image)

    if Main.showSteps == True: # show steps #######################################################
        cv2.imshow("1a", imgGrayscaleScene) #greyscale image
        cv2.imshow("1b", imgThreshScene)  #gaussian image
    # end if # show steps #########################################################################

            # find all possible chars in the scene,
            # this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)  ##function at 125 line ##the list was all possible contour that return true from detectchars.checkIfPossibleChars

    if Main.showSteps == True: # show steps #######################################################
        print("step 2 - len(listOfPossibleCharsInScene) = " + str(
            len(listOfPossibleCharsInScene)))  

        imgContours = np.zeros((height, width, 3), np.uint8)  #create a black image

        contours = []  #initialize an array

        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)  #contours append possibleChar.contour
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE) #(black image,contours[],-1(draw all the contours),(255.0, 255.0, 255.0))
        cv2.imshow("2b", imgContours)
    # end if # show steps #########################################################################

            # given a list of all possible chars, find groups of matching chars
            # in the next steps each group of matching chars will attempt to be recognized as a plate
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)  #goes to DetectChars.py #listOfListsOfMatchingChars回傳回來判斷好的白點群

    if Main.showSteps == True: # show steps #######################################################
        print("step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(
            len(listOfListsOfMatchingCharsInScene)))  # 13 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)

        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            contours = []

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        # end for

        cv2.imshow("3", imgContours)
    # end if # show steps #########################################################################

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   # for each group of matching chars
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)         # attempt to extract plate

        if possiblePlate.imgPlate is not None:                          # if plate was found
            listOfPossiblePlates.append(possiblePlate)                  # add to list of possible plates
        # end if
    # end for

    print("\n" + str(len(listOfPossiblePlates)) + " possible plates found")  # 13 with MCLRNF1 image

    if Main.showSteps == True: # show steps #######################################################
        print("\n")
        cv2.imshow("4a", imgContours)
        ###框車牌
        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = cv2.boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)# 获取最小外接矩形的4个顶点坐标

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)

            print("possible plate " + str(i) + ", click on any image and press a key to continue . . .")

            cv2.imshow("4b", listOfPossiblePlates[i].imgPlate)
            cv2.waitKey(0)
        # end for

        print("\nplate detection complete, click on any image and press a key to begin char recognition . . .\n")
        cv2.waitKey(0)
    # end if # show steps #########################################################################

    return listOfPossiblePlates
# end function

###################################################################################################ok
def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []                # this will be the return value  ##possibleChar intX,intY,intWidth,intHeight爲一組append進去

    intCountOfPossibleChars = 0             

    imgThreshCopy = imgThresh.copy()   ##gaussian image here

    ##cv2.findContours()函数返回两个值，contours是轮廓本身，npaHierarchy是每条轮廓对应的属性。
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # find all contours ##cv2.RETR_LIST检测的轮廓不建立等级关系 #cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标

    height, width = imgThresh.shape   ##gaussian image
    imgContours = np.zeros((height, width, 3), np.uint8)    ##create black image

    for i in range(0, len(contours)):                       # for each contour(輪廓（白點群)

        if Main.showSteps == True: # show steps ###################################################
            cv2.drawContours(imgContours, contours, i, Main.SCALAR_WHITE)
        # end if # show steps #####################################################################

        possibleChar = PossibleChar.PossibleChar(contours[i])   #PossibleChar.py #回傳4個值intX,intY,intWidth,intHeight

        ##checkIfPossibleChar at DetectChars.py 253
        if DetectChars.checkIfPossibleChar(possibleChar):                   # if contour is a possible char, note this does not compare to other chars (yet) . . .(去檢測每一個輪廓是否有包含char)##DetectChars函式庫
            intCountOfPossibleChars = intCountOfPossibleChars + 1           # increment count of possible chars（有的話intCountOfPossibleChars + 1）
            listOfPossibleChars.append(possibleChar)                        # and add to list of possible chars(把contour[i]的值append進去listOfPossibleChars)
        # end if
    # end for

    if Main.showSteps == True: # show steps #######################################################
        print("\nstep 2 - len(contours) = " + str(len(contours)))  # 2362 with MCLRNF1 image
        print("step 2 - intCountOfPossibleChars = " + str(intCountOfPossibleChars))  # 131 with MCLRNF1 image
        cv2.imshow("2a", imgContours)
    # end if # show steps #########################################################################

    return listOfPossibleChars
# end function


###################################################################################################ok
def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value ##回傳PossiblePlate.py内的物件PossiblePlate()

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right based on x position #以listOfMatchingChars（裏面的物件）的屬性intCenterX去做sort

    # calculate the center point of the plate
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0 
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = fltPlateCenterX, fltPlateCenterY #

    # calculate plate width and height #最後一個點-第一個點=等於寬度*1.3
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    #listOfMatchingChar裏面的height 全部相加 
    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)#平均height

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)#平均height*1.5

            # calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY #listOfMatchingChars的CenterY最後一個-listOfMatchingChars的CenterY第一個  ##找到寬度==高度
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1]) #第一個值和最後一個去做彼氏定理 找到char之間的距離
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse) #math.asin=只接受-1到1之間的數字 超出範圍就會回傳NAN##
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)  ##找角度

            # pack plate region center point, width and height, and correction angle into rotated rect member variable of plate
    possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

            # final steps are to perform the actual rotation

            # get the rotation matrix for our calculated correction angle
    rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0) ##(旋轉中心,旋轉角度，縮放比例 ) ##更正字體的角度

    height, width, numChannels = imgOriginal.shape      # unpack original image width and height

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image  ##圖像平移（圖像，變換矩陣，變換后的大小）

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))    ##（imgRotated圖像，（截取圖像高和寬），中心）###回傳圖片

    possiblePlate.imgPlate = imgCropped         # copy the cropped plate image into the applicable member variable of the possible plate ###給值

    return possiblePlate
# end function












