from PIL import Image
import cimap.encoder as encoder
#import cimap.my_io as my_io
import cimap.decoder as decoder
import cimap.my_io as my_io
#import civq.tbenchCIQA as test
from utilities import global_utils as g


def main():
    # Reading file name
    #imageFilename = my_io.getFilename()
    imageFilename = 'cimap/teste4.bmp'

    #N = my_io.getN()
    #M = my_io.getM()
    M = 16
    E = 0.25

    e = encoder.Encoder(M, E)

    img = (Image.open(imageFilename)).convert(mode = "RGB")

    e.buildInitialCodeBook(img)

    #print(e.codebook)    

    #print(list(img.getdata()))

    compressedImage = e.encode(img)

    print("Passei pelo encoder")

    #print(compressedImage)

    my_io.writeCompressed(imageFilename, compressedImage)

    d = decoder.Decoder()

    decompressedImage = d.decode(imageFilename)

    print("Passei pelo decoder")

    img2 = (Image.open(decompressedImage)).convert(mode = "RGB")

    #print(list(img.getdata()))
    #print(list(img2.getdata()))

    imgWidth, imgHeight = img.size
    print(g.calculateMSE(imgWidth, imgHeight, decompressedImage, imageFilename))

if __name__ == "__main__":
    main()