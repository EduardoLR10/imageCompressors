import bitstring

# Get input file name
def getFilename():
    print("Insira o arquivo que sofrerá compressão (com extensão):")
    filename = input()
    return filename

def getN():
    print("Insira o tamanho do lado de cada bloco (N): ")
    N = int(input())
    return N

def getM():
    print("Insira a quantidade de intervalos (M): ")
    M = int(input())
    return M

def writeCompressed(imageFilename, compressed):

    compressedName = imageFilename[:-4] + ".du"

    output = open(compressedName, "wb")

    # Start translation of the original file
    bitArray = ""

    for _list in compressed:
        for elem in _list:
            #print(elem)
            bitArray += elem
    
    # Counting useless bits
    artificialBits = bytes([0])
    
    # Checking if will be necessary to add artificial bits
    if (len(bitArray) % 8):
        quo = int(int(len(bitArray) / 8) + 1)
        artificialBits = bytes([8 * quo - len(bitArray)])

    # Creating bitstream from string
    deployArray = bitstring.BitArray("0b" + bitArray)

    # Writing how many of the final bits are useless
    #output.write(artificialBits)

    # Writing bitstream
    output.write(deployArray.tobytes())

