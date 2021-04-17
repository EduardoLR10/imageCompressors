import PIL
from bitstring import BitArray
import math
import numpy as np
import ciqa.utils as utils

class Decoder:
    
    artifitialBits = 0
    fullHeight = 0
    fullWidth = 0
    N = 0
    M = 0
    outputArray = []

    # Auxiliary variables
    buffer = 0
    buffer2 = 0
    key = ""

    turn = 0
    miN = 0
    delta = 0
    elemCounter = 0

    columnsCounter = 0
    linesCounter = 0

    def __init__(self):
        self.dartifitialBits = 0
        self.fullHeight = 0
        self.fullWidth = 0
        self.N = 0
        self.M = 0
        self.outputArray = []

        # Auxiliary variables
        self.buffer = 0
        self.buffer2 = 0
        self.key = ""

        self.turn = 0
        self.miN = 0
        self.delta = 0
        self.elemCounter = 0

        self.columnsCounter = 0
        self.linesCounter = 0

    def getDecompressedName(self, imageFilename):
        compressedFilename = imageFilename[:-4]
        extension = imageFilename[-4:]
        decompressedFilename = compressedFilename + "Decompressed" + extension
        return decompressedFilename

    def addNewValue(self, value):
        index = int(value, 2)
        rValue = math.ceil(self.miN + utils.getReconstructionValue(index, self.delta))
        self.outputArray.append(rValue)

    def createBlock(self):
        arr = np.array(self.outputArray).reshape((self.N, self.N))
        return PIL.Image.fromarray(arr.astype(np.uint8), 'L')

    def manageIndexes(self):
        if self.columnsCounter == self.fullWidth - self.N:
            #print("oi1")
            self.columnsCounter = 0
            self.linesCounter += self.N
        else:
            self.columnsCounter += self.N
    
    def computeSubImage(self, outputImage):
        #print("buffer = " + str((BitArray(buffer)).bin))
        self.key += (BitArray(self.buffer)).bin
        #print("key0 = " + self.key)
        if self.turn == 0:
            #print(self.key)
            self.miN = int(self.key[:8], 2)
            self.key = self.key[8:]
            #print(self.key)
            #print("miN = " + str(self.miN))
            self.turn = 1
        elif self.turn == 1:
            #print(self.key)
            self.delta = int(self.key[:8], 2)
            self.key = self.key[8:]
            #print(self.key)
            #print("delta = " + str(self.delta))
            self.turn = 2
        else:
            #print("key1 = " + self.key)
            it = ""
            for bit in self.key:
                it += bit
                if len(it) == int(math.log2(self.M)):
                    #print("it, counter = " + str(it) + " " + str(self.elemCounter))
                    self.key = self.key.removeprefix(it)
                    #print("key2 = " + self.key)
                    self.addNewValue(it)
                    if self.elemCounter < (self.N * self.N) - 1:
                        self.elemCounter += 1
                    else:
                        #print("aux, counter, miN, delta: " + str(self.auxCounter) + " " + str(self.elemCounter) + " " + str(self.miN) + " " + str(self.delta))
                        self.elemCounter = 0
                        #print(self.key)
                        #block.show()
                        #print(str(self.columnsCounter) + " " + str(self.linesCounter))
                        block = self.createBlock()
                        outputImage.paste(block, box = (self.columnsCounter, self.linesCounter))
                        self.manageIndexes()
                        self.turn = 0;
                        self.outputArray = []
                        #print(self.key)
                        break
                    it = ""
            
    
    def decode(self, imageFilename):

        # Manipulating strings to generate the new name of the decompressed file
        decompressedFilename = self.getDecompressedName(imageFilename)
        input = open(imageFilename[:-4] + ".du", "rb")

        # Reading the artifitial bits of the last byte of the compressed file
        #self.artifitialBits = int.from_bytes(input.read(1), "big")

        # Getting important metrics from file
        self.fullHeight = int.from_bytes(input.read(2), "big")
        self.fullWidth = int.from_bytes(input.read(2), "big")
        self.N = int.from_bytes(input.read(1), "big")
        self.M = int.from_bytes(input.read(1), "big")

        #print(self.artifitialBits)
        #print(self.fullHeight)
        #print(self.fullWidth)
        #print(self.N)
        #print(self.M)

        outputImage = PIL.Image.new(mode = "L", size = (self.fullWidth, self.fullHeight))

        # Start reading the content of the compressed one and writing the decompressed file
        self.buffer = input.read(1)
        if self.buffer:
            while True:
                self.buffer2 = input.read(1)
                # If the second read was not sucessful, it means that buffer contains the last byte of the compressed file
                if not self.buffer2:
                    #print("oiZ")
                    if self.artifitialBits:
                        #print("oiY")
                        self.key = self.key[:(-self.artifitialBits)]
                    #print("buffer = " + str((BitArray(self.buffer)).bin))
                    #print("oi2")
                    #self.key += "0"
                    while self.key != "" or self.buffer != 0:
                        self.computeSubImage(outputImage)
                        self.buffer = 0
                    break
                else:
                    self.computeSubImage(outputImage)
                        
                self.buffer = self.buffer2

        
        outputImage.save(decompressedFilename)
        #print("salvei minha imagem e acabou")
        return decompressedFilename