from PIL import Image
import math
import matplotlib.pyplot as plt
import ciqa.encoder as encoder
import ciqa.decoder as decoder
import ciqa.my_io as my_io
from utilities import global_utils as g
from utilities import config as c

def test_and_plot(imageFilename):
    original = (Image.open(imageFilename)).convert(mode = "L")

    N = [4, 8, 16, 32]
    M = [2, 4, 8, 16]

    bppS = []
    mseS = []

    imgWidth, imgHeight = original.size

    for n in N:
        aux_b = []
        aux_m = []
        for m in M:
            e = encoder.Encoder(m, n)

            compressedImage = e.encode(original)

            my_io.writeCompressed(imageFilename, compressedImage)

            d = decoder.Decoder()

            decompressedImagename = d.decode(imageFilename)

            mse = g.calculateMSE(imgWidth, imgHeight, decompressedImagename, imageFilename)
            psnr = g.calculatePSNR(mse, c.ColorType.GRAYSCALE)

            bpp = (48 + ((imgHeight * imgWidth) / (n * n)) * (16 + (math.log2(m) * n * n))) / (imgHeight * imgWidth)

            print("Calculating to N = %d and M = %d with MSE = %lf, PSNR = %lf and bpp = %lf" % (n, m, mse, psnr, bpp))

            aux_b.append(bpp)

            aux_m.append(mse)

            del e
            del d

        bppS.append(aux_b)

        mseS.append(aux_m)

    #print(bppS)
    #print(mseS)

    styles = ['r-', 'b-', 'g-', 'k-']

    lines = ['N = 4', 'N = 8', 'N = 16', 'N = 32']


    for i in range(0, len(N)):
        plt.plot(bppS[i], mseS[i], styles[i], label = lines[i])

    plt.legend()
    plt.xlabel('bpp')
    plt.ylabel('MSE')

    plt.show()