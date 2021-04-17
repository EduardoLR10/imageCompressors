import math
#import civq.utils as utils
import sys
from statistics import mean

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

    def __init__(self, m, l, e):
        self.M = m
        self.L = l
        self.epslon = e
        self.codebook = self.getInitialCodeBook()

    def getInitialCodeBook(self):

        initialCodeBook = []

        step = int((256 / self.M) / self.L)

        counter = 1
        l = []
        for j in range(0, 256, step):
            l.append(j)
            if(not (counter % self.L)):
                initialCodeBook.append(l)
                l = []
            counter += 1
    
        return initialCodeBook
    
    def calculateDistortion(self, v1, v2):

        size = len(v1)

        print(v1)
        print(v2)

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
        for vector in vectors:
            chosen = self.findClosest(vector)
        
            updatedValue = [vector]

            if chosen in self.regions:
                for already in self.regions[chosen]:
                    updatedValue.append(already)

            self.regions.update({chosen : updatedValue})

    def calculateAverageDistortion(self, size):
        avg_dist = 0

        print(self.regions)
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
            size = len(values[0])
            avg = [0] * size
            for i in range(0, len(values[0])):

                for vector in values:
                    avg[i] += vector[i]

                avg[i] //= size 

            self.codebook[indexKey] = avg

    def encode(self, img):

        print(self.codebook)

        vectors = []

        side = int(math.sqrt(self.L))

        imgWidth, imgHeight = img.size

        height = side
        width = side

        ## STEP 1 ##
        
        # Generating vectors from image
        for i in range(0, imgHeight // side):
            for j in range(0, imgWidth // side):
                #print(str(j * width) + " " + str(i * height) + " " + str((j + 1) * width) + " " + str((i + 1) * height))
                box = (j * width, i * height, ((j + 1) * width), ((i + 1) * height))
                cropped = img.crop(box)
                
                vectors.append(list(cropped.getdata()))
        
        # Starting list of distortions for future comparison
        distortions = [0]

        ## STEP 2 ##
        
        # Allocating vector into their regions
        self.allocateRegions(vectors)
        print(self.regions)
        ## STEP 3 ##
        
        # Adding second distortion to start interation
        size = len(vectors)
        distortions.append(self.calculateAverageDistortion(size))
        print(distortions)
        ## STEP 4 ##

        # Updating codebook until error condition is satisfied
        counter = 1
        print(((distortions[counter] - distortions[counter - 1]) / distortions[counter]))
        while(((distortions[counter] - distortions[counter - 1]) / distortions[counter]) > self.epslon):
            self.updateCodeBook()
            print("oi1")
            print(self.codebook)
            next = self.calculateAverageDistortion(size)
            print(next)
            distortions.append(next)
            print(distortions)
            counter += 1

        # Making a list from region dictionary
        dictList = []
        for key, value in self.regions.items():
            temp = [key,value]
            dictList.append(temp)   

        # Need to send the codebook!
        return (self.codebook, dictList)
        