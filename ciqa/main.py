from PIL import Image
import ciqa.encoder as encoder
import ciqa.my_io as my_io
import ciqa.decoder as decoder
import ciqa.tbenchCIQA as test
from utilities import global_utils as g


def main():
    # Reading file name
    #imageFilename = my_io.getFilename()
    imageFilename = 'ciqa/lena.bmp'

    test.test_and_plot(imageFilename)
    return

    #N = my_io.getN()
    #M = my_io.getM()
    N = 4
    M = 2

    img = (Image.open(imageFilename)).convert(mode = "L")

    e = encoder.Encoder(M, N)

    compressedImage = e.encode(img)

    #print(compressedImage)

    my_io.writeCompressed(imageFilename, compressedImage)

    d = decoder.Decoder()

    decompressedImage = d.decode(imageFilename)

    imgWidth, imgHeight = img.size
    print(g.calculateMSE(imgWidth, imgHeight, decompressedImage, imageFilename))

    #result = (Image.open(decompressedImage)).convert(mode = "L")
    ''' print(decompressedImage)

    box = (72, 504, 76, 508)
    cropped = img2.crop(box)

    #cropped.show()

    print(list(cropped.getdata())) '''

if __name__ == "__main__":
    main()