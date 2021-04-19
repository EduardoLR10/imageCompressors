from PIL import Image
import civq.encoder as encoder
#import civq.my_io as my_io
import civq.decoder as decoder
import civq.my_io as my_io
#import civq.tbenchCIQA as test
from utilities import global_utils as g


def main():
    # Reading file name
    #imageFilename = my_io.getFilename()
    imageFilename = 'civq/lena.bmp'

    #N = my_io.getN()
    #M = my_io.getM()
    M = 256
    L = 4
    E = 0.025

    e = encoder.Encoder(M, L, E)

    img = (Image.open(imageFilename)).convert(mode = "L")

    compressedImage = e.encode(img)

    #print(compressedImage)

    my_io.writeCompressed(imageFilename, compressedImage)

    d = decoder.Decoder()
    decompressedImage = d.decode(imageFilename)

    """ img2 = (Image.open(decompressedImage)).convert(mode = "L")

    print(list(img.getdata()))
    print(list(img2.getdata()))

    imgWidth, imgHeight = img.size
    print(g.calculateMSE(imgWidth, imgHeight, decompressedImage, imageFilename)) """
    """ 
     """

    #result = (Image.open(decompressedImage)).convert(mode = "L")
    ''' print(decompressedImage)

    box = (72, 504, 76, 508)
    cropped = img2.crop(box)

    #cropped.show()

    print(list(cropped.getdata())) '''

if __name__ == "__main__":
    main()