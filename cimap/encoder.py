import math
#import civq.utils as utils
import sys
import civq.utils as utils
import numpy as np

class Encoder:
    # Codebook's size
    M = 0

    # Block's area
    L = 0

    # Stop condition
    epslon = 0

    # Codebook
    codebook = []

    # Regions to associate vector with codebook vectors
    regions = {}
    indexReconstruct = {}

    def __init__(self, m, e):
        self.M = m
        self.L = 3
        self.epslon = e
        self.codebook = []
        #print(self.codebook)

    def buildInitialCodeBook(self, img):

        imgWidth, imgHeight = img.size

        initialCodeBook = []

        if imgHeight * imgWidth >= self.M:
            l = list(img.getdata())
            step = len(l) // self.M
            for i in range(0, len(l), step):
                r, g, b = l[i]
                initialCodeBook.append([r,g,b])
        else:
            initialCodeBook = self.getUniformInitialCodeBook()

        self.codebook = initialCodeBook

    def getUniformInitialCodeBook(self):

        initialCodeBook = []

        product = self.M * self.L

        if product <= 256:
            step = int((256 / self.M) / self.L)

            counter = 1
            l = []
            for j in range(0, 256, step):
                l.append(j)
                if(not (counter % self.L)):
                    initialCodeBook.append(l)
                    if len(initialCodeBook) == self.M:
                        break
                    l = []
                counter += 1
        else:
            repetition = product // 256
            #print(repetition)
            l = []
            done = False
            counter = 0
            for j in range(0, 256):
                for k in range(0, max(repetition, 2)):
                    l.append(j)
                    counter += 1
                    if(not (counter % self.L)):
                        #print(counter)
                        #print(l)
                        initialCodeBook.append(l)
                        if len(initialCodeBook) == self.M:
                            done = True
                            break
                        l = []
                    #print(l)
                if done:
                    break
        
        return initialCodeBook
    
    def calculateDistortion(self, v1, v2):

        size = len(v1)

        #print(v1)
        #print(v2)

        mse = 0
        for i in range(0, size):
            mse += math.pow(v1[i] - v2[i], 2)

        mse /= size

        return mse

    def findClosest(self, v1):
        distortion = sys.float_info.max
        index = 0
        #print(self.codebook)
        counter = 0
        for vector in self.codebook:
            result = self.calculateDistortion(v1, vector)
            if(result < distortion):
                distortion = result
                index = counter
            counter += 1

        return index

    def allocateRegions(self, vectors):
        self.regions = {}
        self.indexReconstruct = {}
        counter = 0
        for vector in vectors:
            chosen = self.findClosest(vector)
        
            updatedValue = [vector]

            if chosen in self.regions:
                for already in self.regions[chosen]:
                    updatedValue.append(already)

            self.regions.update({chosen : updatedValue})
            self.indexReconstruct.update({counter : chosen})
            counter += 1

    def calculateAverageDistortion(self, size):
        avg_dist = 0

        #print(self.regions)
        keys = self.regions.keys()
        for index in keys:
            values = self.regions[index]
            for allocated in values:
                avg_dist += self.calculateDistortion(allocated, self.codebook[index])
            
        avg_dist /= size

        return avg_dist

    def updateCodeBook(self):
        for indexKey in self.regions.keys():
            values = self.regions[indexKey]
            quantity = len(values)
            sizeOfEach = len(values[0])
            #print(sizeOfEach)
            avg = [0] * sizeOfEach
            for i in range(0, len(values[0])):

                for vector in values:
                    avg[i] += vector[i]

                avg[i] //= quantity
            #print(avg)
            self.codebook[indexKey] = avg
        #print(self.codebook)

    def encode(self, img):

        #print(self.codebook)

        pixels = []

        imgWidth, imgHeight = img.size

        ## STEP 1 ##
        
        # Generating vectors from image
        for r, g, b in list(img.getdata()):
            pixels.append([r, g, b])

        # Starting list of distortions for future comparison
        distortions = [0]

        ## STEP 2 ##
        
        # Allocating vector into their regions
        self.allocateRegions(pixels)
        #print(self.regions)
        ## STEP 3 ##
        
        # Adding second distortion to start interation
        size = len(pixels)
        distortions.append(self.calculateAverageDistortion(size))
        #print(distortions)
        ## STEP 4 ##

        # Updating codebook until error condition is satisfied
        counter = 1
        if distortions[counter] != 0.0:
            #print(((distortions[counter] - distortions[counter - 1]) / distortions[counter]))
            while(abs((distortions[counter] - distortions[counter - 1]) / distortions[counter]) > self.epslon):

                ## STEP 5 ##
                self.updateCodeBook()

                ## BACK TO STEP 2 ##
                self.allocateRegions(pixels)

                ## STEP 3 ##
                next = self.calculateAverageDistortion(size)
                if next == 0.0:
                    break
                #print(next)
                distortions.append(next)
                print(distortions)
                counter += 1

        # Making a list from region dictionary
        indexList = []
        """ for key, value in self.regions.items():
            temp = (key,value)
            dictList.append(temp)    """
        
        for i in range(0, len(pixels)):
            indexList.append(self.indexReconstruct[i])

        #print(self.regions)
        #print(indexList)
        # Need to send the codebook!
        #print(self.codebook)
        return (imgHeight, imgWidth, self.M - 1, self.codebook, indexList)
        