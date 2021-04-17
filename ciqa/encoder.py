import ciqa.utils as utils
import numpy as np
import math

class Encoder:
    # Number of bins
    M = 0

    # Size of square to encode
    N = 0

    def __init__(self, m, n):
        self.M = m
        self.N = n

    def quantify(self, img):
        data = list(img.getdata())
        #print(data)
        miN = min(data)
        maX = max(data)
        delta = max((maX - miN) // self.M, 1)
        #print("min, max e delta: " + str(miN) + " " + str(maX) + " " + str(delta))
        return miN, delta

    def encode(self, img):

        encode = []

        #print(list(img.getdata()))
        #print(img.size)
        imgWidth, imgHeight = img.size
        height = self.N
        width = self.N
        for i in range(0, imgHeight // self.N):
            for j in range(0, imgWidth // self.N):
                #print(str(j * width) + " " + str(i * height) + " " + str((j + 1) * width) + " " + str((i + 1) * height))
                box = (j * width, i * height, ((j + 1) * width), ((i + 1) * height))
                cropped = img.crop(box)
                #cropped.show()
                miN, delta = self.quantify(cropped)

                l = []
                l.append(utils.mString(miN, 8))
                l.append(utils.mString(delta, 8))

                #cropped.save("teste" + str(i) + str(j) + ".bmp")
                #cropped.show()
                #print(cropped.size)
                for pixel in (list(cropped.getdata())):
                    k_1 = miN
                    k = k_1 + delta
                    index = 0
                    while (not (pixel >= k_1 and pixel < k)) and index + 1 < self.M:
                        k_1 = k
                        k += delta
                        index += 1
                    #if index != 1 and index != 0:
                        #print("deu ruim! " + str(miN) + " " + str(pixel) + " " + str(delta) + " " + str(index))
                    l.append(utils.mString(index, int(math.log2(self.M))))
        
                encode.append(l)

        
        return ([utils.mString(imgHeight, 16), utils.mString(imgWidth, 16), utils.mString(self.N, 8), utils.mString(self.M, 8)] + encode)