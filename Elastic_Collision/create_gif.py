import os
from PIL import Image
import subprocess
import imageio
def filecount():
    totalFiles = 0
    for base, dirs, files in os.walk("GIF_Dump/"):
        print('Searching in : ', base)
        for Files in files:
            totalFiles += 1
    print(totalFiles)
    return totalFiles

def convert():
    totalFiles = filecount()
    bound = totalFiles
    percent = 5
    for i in range(1, totalFiles + 1):
        filename = "GIF_Dump/{}".format(i)

        img = Image.open(filename + '.eps')

        img.save(filename + '.jpg')
        img.close()
        subprocess.run("rm " + filename + ".eps")
        if (i/bound*100 >= percent):
            print("\r",percent, "% Images Converted to Jpeg Format", end = "")
            percent += 5
    print()

def resolutions():
    filenames = ["GIF_Dump/" + str(i) + ".jpg" for i in range(1, filecount() + 1)]
    for imag in filenames:
        img = Image.open(imag)

        # fetching the dimensions
        wid, hgt = img.size

        # displaying the dimensions
        print(imag, " --> ",str(wid) + "x" + str(hgt))


def merge(outfile):

    filenames = ["GIF_Dump/" + str(i) + ".jpg" for i in range(1, filecount() + 1)]
    bound = len(filenames)
    percent = 5
    with imageio.get_writer('Output/Gifs/{}.gif'.format(outfile), mode='I') as writer:
        count = 1
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
            subprocess.run("rm " + filename)
            if (count / bound * 100 >= percent):
                print("\r", percent, "% Images Merged to Gif and Removed", end="")
                percent += 5
            count += 1
    print()

def gifconversion(outfile = "Demo"):
    convert()
    merge(outfile)

# merge("10m50M10v10V")