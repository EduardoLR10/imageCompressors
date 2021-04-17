from PIL import Image
import math
from utilities import config as c

def calculateMSE(m, n, testImgName, referenceImgName):

    testImg = (Image.open(testImgName)).convert(mode = "L")
    referenceImg = (Image.open(referenceImgName)).convert(mode = "L")

    t = testImg.load()
    r = referenceImg.load()

    mse = 0
    for i in range(0, n):
        for j in range(0, m):
            mse += math.pow(t[i, j] - r[i, j], 2)

    mse /= m * n

    return mse

def calculatePSNR(mse, color):
    if color == c.ColorType.GRAYSCALE:
        return 10 * math.log10((math.pow(255 , 2)) / mse)

