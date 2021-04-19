import bitstring
import civq.utils as utils
import math as m

# Get input file name
def getFilename():
    print("Insira o arquivo que sofrerá compressão (com extensão):")
    filename = input()
    return filename

def getL():
    print("Insira a área de cada bloco (L): ")
    L = int(input())
    return L

def getM():
    print("Insira o tamanho do codebook (M): ")
    M = int(input())
    return M

def writeCompressed(imageFilename, compressed):

    compressedName = imageFilename[:-4] + ".du"

    output = open(compressedName, "wb")

    height, width, L, M, codebook, indexes = compressed

    # Start translation of the original file
    bitArray = ""

    bitArray += utils.mString(height, 16)

    bitArray += utils.mString(width, 16)

    bitArray += utils.mString(L, 8)

    bitArray += utils.mString(M, 8)

    for vector in codebook:
        for elem in vector:
            bitArray += utils.mString(elem, 8)

    for index in indexes:
        #print(index)
        #print(utils.mString(index, int(m.log2(M))))
        bitArray += utils.mString(index, int(m.log2(M + 1)))

    # Counting useless bits
    artificialBits = bytes([0])
    
    # Checking if will be necessary to add artificial bits
    if (len(bitArray) % 8):
        quo = int(int(len(bitArray) / 8) + 1)
        artificialBits = bytes([8 * quo - len(bitArray)])

    # Creating bitstream from string
    deployArray = bitstring.BitArray("0b" + bitArray)
    #print(artificialBits)
    # Writing how many of the final bits are useless
    output.write(artificialBits)

    # Writing bitstream
    output.write(deployArray.tobytes())

