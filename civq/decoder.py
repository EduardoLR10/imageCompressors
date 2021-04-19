import PIL
from bitstring import BitArray
import math as m
import numpy as np

class Decoder:

    codebook = {}
    it = ""
    columnsCounter = 0
    linesCounter = 0

    side = 0

    def __init__(self):
        self.codebook = {}
        self.it = ""
        self.columnsCounter = 0
        self.linesCounter = 0
        self.side = 0

        self.artifitialBits = 0
        self.fullHeight = 0
        self.fullWidth = 0
        self.L = 0
        self.M = 0

    def getDecompressedName(self, imageFilename):
        compressedFilename = imageFilename[:-4]
        extension = imageFilename[-4:]
        decompressedFilename = compressedFilename + "Decompressed" + extension
        return decompressedFilename

    def composeSubImage(self, outputImage):
        
        #print(self.it)
        arr = np.array(self.codebook[int(self.it, 2)]).reshape((self.side, self.side))
        block = PIL.Image.fromarray(arr.astype(np.uint8), 'L')

        outputImage.paste(block, box = (self.columnsCounter, self.linesCounter))

        if self.columnsCounter == self.fullWidth - self.side:
                #print("oi1")
            self.columnsCounter = 0
            self.linesCounter += self.side
        else:
            self.columnsCounter += self.side
        
        return outputImage

    def decode(self, imageFilename):
        
        # Manipulating strings to generate the new name of the decompressed file
        decompressedFilename = self.getDecompressedName(imageFilename)
        input = open(imageFilename[:-4] + ".du", "rb")

        # Reading the artifitial bits of the last byte of the compressed file
        self.artifitialBits = int.from_bytes(input.read(1), "big")

        # Getting important metrics from file
        self.fullHeight = int.from_bytes(input.read(2), "big")
        self.fullWidth = int.from_bytes(input.read(2), "big")
        self.L = int.from_bytes(input.read(1), "big")
        self.M = int.from_bytes(input.read(1), "big") + 1
        self.side = int(m.sqrt(self.L))

        #print(self.artifitialBits)
        #print(self.fullHeight)
        #print(self.fullWidth)
        #print(self.L)
        #print(self.M)

        for i in range(0, self.M):
            vector = []
            for j in range(0, self.L):
                vector.append(int.from_bytes(input.read(1), "big"))
            self.codebook.update({i : vector})

        #print(self.codebook)

        outputImage = PIL.Image.new(mode = "L", size = (self.fullWidth, self.fullHeight))

        # Start reading the content of the compressed one and writing the decompressed file
        buffer = input.read(1)
        if buffer:
            while True:
                buffer2 = input.read(1)
                # If the second read was not sucessful, it means that buffer contains the last byte of the compressed file
                if not buffer2:
                    #print((BitArray(buffer)).bin)
                    bitArray = (BitArray(buffer)).bin

                    # In this case, we just read the bits that we know are useful
                    for i in range(0, len(bitArray) - self.artifitialBits):
                        self.it += str(bitArray[i])
                        if len(self.it) == int(m.log2(self.M)):
                            #print(self.it)
                            outputImage = self.composeSubImage(outputImage)
                            self.it = ""
                        
                    break
                else:
                    #print((BitArray(buffer)).bin)
                    for bit in (BitArray(buffer)).bin:
                        self.it += bit
                        #print(len(self.it))
                        #print(int(m.log2(self.M)))
                        if len(self.it) == int(m.log2(self.M)):
                            #print(self.it)
                            outputImage = self.composeSubImage(outputImage)
                            self.it = ""
                    #print(self.it)
                buffer = buffer2

        
        outputImage.save(decompressedFilename)
        print("salvei minha imagem e acabou")
        return decompressedFilename