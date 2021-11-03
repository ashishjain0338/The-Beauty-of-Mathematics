import turtle
import subprocess

def getDirection(curve):
    '''It converts the Integer Direction into LDR format, Integer to LDR mapping is as follows
        0 --> Up (U)
        1 --> Right (R)
        2 --> Down (D)
        3 --> Left (L)
        '''
    path = ""
    key = "URDL"
    for codes in curve:
        path = path + key[codes]
    return path


def shift90(path):
    '''It shifts the cell by 90 degrees and also exchanges U with D in order to draw the curve 90 rotated in reverse order'''
    for i in range(0, len(path)):
        path[i] = (path[i] + 1) % 4
        if(path[i] == 0):
            path[i] = 2
        elif (path[i] == 2):
            path[i] = 0
    return path

def shift270(path):
    '''It shifts the cell by -90 degrees and also exchanges U with D in order to draw the curve -90 rotated in reverse order'''
    for i in range(0, len(path)):
        path[i] = (path[i] - 1) % 4
        if(path[i] == 0):
            path[i] = 2
        elif (path[i] == 2):
            path[i] = 0
    return path

def getcurve(n):
    '''It is a recursive fxn that generates the next stage of hilbert curve
        cell --> (n - 1) degree Psuedo Hilbert Curve
        1) Rotate the cell at 90 degrees.
        2) Go Up
        3) Same Cell
        4) Go Right
        5) Same Cell
        6) Go Down
        7) Rotate the cell by 270 degrees.
        '''
    if n == 1:
        return [0, 1, 2]

    current = getcurve(n - 1)
    out = shift90(current[:])
    out.append(0)
    out.extend(current)
    out.append(1)
    out.extend(current)
    out.append(2)
    out.extend(shift270(current[:]))

    return out

def codeToList(path):
    '''For testing purposes, It convert the directions in LDR format to integer lists'''
    code = "URDL"
    return [code.index(x) for x in path]


def captureImage(pen, filename):
    '''Save the Turtle output'''
    filename = "Images/" + filename
    canvas = pen.getscreen().getcanvas()
    canvas.postscript(file = filename + ".ps")

def convertPStoPNG(filename):
    '''This is for conversion of Postscript image to png format'''
    cmd = "gswin64 -sDEVICE=png16m -o " + filename + ".png " + filename + ".ps"
    print(cmd)
    subprocess.run(cmd)
    subprocess.run("rm " + filename + ".ps")

def drawcode(code, weight, background_color = "#EDE6DB", pen_color = "purple", title = "Hilbert Curve", imageFile = None):
    '''It draws the curve according to the LDR code and weigth here represents the length ot one step size'''
    wn = turtle.Screen()
    wn.bgcolor(background_color)
    wn.title(title)

    pen = turtle.Turtle()
    # pen.speed(0)
    pen.color(pen_color)
    TURTLE_SIZE = 20
    pen.up()
    pen.goto(TURTLE_SIZE - wn.window_width() / 2, - (wn.window_height() / 2 - TURTLE_SIZE))# Setting the pen to Bottom Left Corner
    # pen.goto(-300,-200)
    pen.down()


    for drn in code:
        arrow = {'L' : 180 , 'U' : 90, 'R' : 0 , 'D' : 270}
        pen.setheading(arrow[drn])
        pen.fd(weight)
    if (imageFile != None):
        captureImage(pen, imageFile)
    turtle.done()
    if( imageFile != None):
        convertPStoPNG(imageFile)

if __name__ == '__main__':
    degree  = int(input("Enter the degree of Hilbert Curve You want to Draw : "))
    width = int(input("Enter the Step Size : "))

    drn = getDirection(getcurve(degree))
    print("The Required Blueprint of Degree {} Hilbert Curver are ".format(degree), drn)
    print("Total Number of lines are --> ", len(drn))
    print("Total perimetre --> ", len(drn)*width, " Units")
    print("Drawing the Required Hilbert Curve")
    drawcode(drn, width)


