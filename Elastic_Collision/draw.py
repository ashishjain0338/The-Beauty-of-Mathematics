import turtle
import subprocess
import simplejson as json
import numpy as np
from math import pi
from PIL import Image


def captureImage(pen, filename):
    '''Save the Turtle output'''
    canvas = pen.getscreen().getcanvas()
    canvas.postscript(file = filename + '.eps')
    img = Image.open(filename + '.eps')
    img.save(filename + '.jpg')
    img.close()
    subprocess.run("rm " + filename + ".eps")

def convertPStoPNG(filename):
    '''This is for conversion of Postscript image to png format'''
    cmd = "gswin64 -sDEVICE=png16m -o " + filename + ".png " + filename + ".ps"
    print(cmd)
    subprocess.run(cmd)
    subprocess.run("rm " + filename + ".ps")

def lineplot(cord, pen,magx = 1, magy = 1,cenx = 0, ceny = 0, pen_color = "white"):
    '''For Plotting Line Plots as it happens in Matpltolib'''
    pen.color(pen_color)
    pen.up()
    pen.goto(cenx + cord[0][0] * magx, ceny + cord[0][1] * magy)
    pen.down()
    for i in range(1, len(cord)):
        pen.goto(cenx + cord[i][0] * magx, ceny + cord[i][1] * magy)


def fitToScreen(a, b, fixa = 125, fixb = 125, stretch = False):
    '''
        It Fits the PLot to screen by Stretching one axes to completely fit the screen axis (fixa, fixb),
            and increasing other axis by a factor to maintain same aspect ratio
        When Strectch is Truw then Aspect Ratio is Compromised and Both the axes are fit to screen
    '''
    if stretch:
        return (fixa / a, fixb / b)

    if(a > b):
        return (fixa/a, fixa/a)
    else:
        return (fixb/b, fixb/b)


def drawEllipse(pen,  a, b, cenx = 0, ceny = 0, pen_color = "white", fitscreen = False, stretch = False):
    '''
        Draws the Ellipse defined by
            Center --> (cenx, ceny)
            a and b
    '''
    t = np.linspace(0, 2 * pi, 100)
    if fitscreen:
        (magx, magy) = fitToScreen(a, b, stretch=stretch)
    else:
        magx = 1
        magy = 1
    # print(magx, magy)
    (x, y) = (cenx + a*np.cos(t)*magx , ceny + b*np.sin(t)*magy)
    pen.color(pen_color)
    pen.up()
    pen.goto(x[0] , y[0] )
    pen.down()
    for i in range(1, len(x)):
        pen.goto(x[i] , y[i] )


def starter(data,cenx = 0, ceny = 0,background_color = "#000000", pen_color = "white", title = "Plot of v2 VS v1 (Elastic Collision)", imageFile = None):
    wn = turtle.Screen()
    wn.bgcolor(background_color)
    wn.title(title)
    pen = turtle.Turtle()
    big = turtle.Turtle()
    big.color("white")
    small = turtle.Turtle()
    small.color("white")
    big.shape("square")
    small.shape("square")
    small.fd(100)


    pen2 = turtle.Turtle()
    drawEllipse(pen2, 150, 150, cenx= cenx, ceny= ceny, pen_color="yellow", fitscreen=True)
    drawEllipse(pen2, data['a'], data['b'], cenx=cenx, ceny=ceny, pen_color="red", fitscreen=True, stretch = True)
    (x,y) = fitToScreen(data['a'], data['b'], stretch=True)
    lineplot(data['data'], pen, magx = x, magy = y, cenx = cenx, ceny = ceny)



    if (imageFile != None):
        captureImage(pen, imageFile)
    turtle.done()
    if( imageFile != None):
        convertPStoPNG(imageFile)





if(__name__ == "__main__"):
    inputfile = "100m1u.json"
    with open(inputfile, 'r') as fp:
        data = json.load(fp)