import turtle
import simplejson as json
from draw import drawEllipse, fitToScreen, captureImage, convertPStoPNG


def drawsurface(pen, height, width, pen_color="white"):
    '''Draws the Wall and Floor Surface'''
    pen.speed(0)
    pen.up()
    pen.color(pen_color)
    pen.goto(-width / 2 + 40, height / 2)
    step = 50 # For Drawing the Slant Lines
    for i in range(0, height - 100, step):
        pen.setheading(270)
        pen.down()
        pen.fd(step)
        pen.setheading(245)
        pen.up()
        pen.fd(20)
        pen.down()
        pen.fd(40)
        pen.up()
        pen.left(180)
        pen.fd(60)

    for i in range(0, width - 100, step):
        pen.setheading(0)
        pen.down()
        pen.fd(step)
        pen.setheading(225)
        pen.up()
        pen.fd(20)
        pen.down()
        pen.fd(40)
        pen.up()
        pen.left(180)
        pen.fd(60)


def scale(p, lmax, c=10, d=20):
    '''It Scales up the Actual velocities to the range [c, d] so that Collisions could be detected within limit'''
    neg = False
    if p == 0:
        return p
    if p < 0:
        neg = True
    p = abs(p)
    num = (c + (d - c) * p / lmax)
    if neg:
        return -num
    return num


def write_score(writer, text, move, start, rightwall, heading=False, hdis=100):
    '''Writes the data in the Up Table,
        It is Made Smart, That It would change line Automatically when needed
        '''
    rightwall = rightwall - 310  # For Ellipse (250 for stretch + 50 for axes + 10 for safe separation)

    # Checking For New Line
    if (abs(writer[0].xcor() - rightwall) < move[0]):
        print("Need to go to next line", text)
        line_num = (start[1] - writer[0].ycor()) / move[1] / 4
        for i in range(0, len(writer)):
            writer[i].up()
            writer[i].goto(hdis + start[0], start[1] - move[1] * 4 * (line_num + 1) - move[1] * i)
            writer[i].down()

    # Writing the Data in Up table
    for i in range(0, len(writer)):
        writer[i].write(text[i], font=("Calibri", 15, "bold"))
        writer[i].up()
        if (heading):
            writer[i].fd(hdis)
        else:
            writer[i].fd(move[0])
        writer[i].down()


def ellipse_screen(pen, cenx, ceny, a, b, spread, pen_color="white"):
    '''For Drawing the x-y axis for Ellipse Plot'''
    pen.color(pen_color)
    pen.up()
    pen.goto(cenx - a - spread, ceny + b + spread)
    pen.down()
    pen.setheading(270)
    pen.fd(2 * b + 2 * spread)
    pen.left(90)
    pen.fd(2 * a + 2 * spread)
    pen.up()
    pen.goto(cenx - a - spread - 30, ceny)
    pen.write("v1", font=("Calibri", 15, "bold"))
    pen.goto(cenx, ceny - b - spread - 30)
    pen.write("v2", font=("Calibri", 15, "bold"))




def simulate(data, writer, pens, specs,settings,limiter = 2000):
    '''It Simulates the Collision'''
    # Retreieving the data of the screen
    a = data['a']
    b = data['b']
    speed = data['data']
    (move, start, rightwall, leftwall) = (specs["move"], specs["start"], specs["rightwall"], specs["leftwall"])
    (cenx, ceny, magx, magy) = (specs["cenx"], specs["ceny"], specs["magx"], specs["magy"])
    big = pens[1]
    small = pens[2]
    limit = specs["limit"]

    # Starting the Simulation sv,bv represents velocities of small and big block
    (sv, bv) = (scale(speed[0][1], max(a, b)), scale(speed[0][0], max(a, b)))
    if settings["show-table-data"]:
        write_score(writer, [0, round(speed[0][1], 2), round(speed[0][0], 2)], move, start, rightwall)
    sd = 0
    bd = 60
    zoom_written = False
    num = 1
    if(len(speed) == 1):
        return
    if(speed[0][1] != speed[1][1] and abs(speed[0][1]) == abs(speed[1][1])):
        waitwall = True
    else:
        waitwall = False
    print("Waitwall here ", waitwall)
    # THE SIMULATION
    for i in range(limiter):
        if (abs(bd - rightwall) < limit):
            # If the Big Block Reaches the Rightwall, Speed Up the Simulation
            bv = 0
            if not zoom_written:
                pens[6].setheading(90)
                pens[6].fd(25)
                pens[6].up()
                pens[6].fd(10)
                pens[6].setheading(180)
                pens[6].fd(50)
                pens[6].write("Speeding Up\n Zooming Out", font=("Calibri", 10, "bold"))
                zoom_written = True

        # Alternately Move Blocks
        if i % 2 == 1:
            small.fd(sv)
            sd = sd + sv
        else:
            big.fd(bv)
            bd = bd + bv

        col_hap = True
        while col_hap:
            col_hap = False
            if waitwall:
                # Checking Collision with the Wall
                if (abs(sd - leftwall) <= limit):
                    print("Collision ,", num, ",with the Wall")
                    if settings["show-plot"]:
                        pens[0].goto(cenx + speed[num][0] * magx, ceny + speed[num][1] * magy)
                    num = num + 1
                    sv = - sv
                    waitwall = False
                    col_hap = True
            else:
                # Checking Collision within the blocks
                if (abs(sd - bd) <= limit):
                    print("Collision ,", num, ",within blocks")
                    (sv, bv) = (scale(speed[num][1], max(a, b)), scale(speed[num][0], max(a, b)))
                    if settings["show-plot"]:
                        pens[0].goto(cenx + speed[num][0] * magx, ceny + speed[num][1] * magy)
                    num = num + 1
                    waitwall = True
                    col_hap = True

            if col_hap:
                # Writing the data in Table Up
                if settings["show-table-data"]:
                    write_score(writer, [num - 1, round(speed[num - 1][1], 2), round(speed[num - 1][0], 2)], move, start,
                            rightwall)
                # Speeding Up the Simulation
                if zoom_written and settings["speed-at-last"] and waitwall:
                    sv = (rightwall - leftwall - limit) / 4 * (sv / abs(sv))
                    small.speed(7)
                    print("Speeding Up ", sv)
            if (bv > 0):
                break

        if (num == len(speed)):
            break
    # For Some After-Effects
    for i in range(0, 20):
        small.fd(sv)
        big.fd(bv)
    if(num != len(speed)):
        print("Simulation Can't Run Fully, Increase the Limiter to run it properly !!")


def starter(data, settings, imagefile = None):
    '''This Function generates all the pen and screens'''
    # Setting up the window
    wn = turtle.Screen()
    wn.setup(width=1.0, height=1.0) # For Fullscreen
    # wn.bgcolor("black")
    wn.title("Collide")
    h = wn.window_height()
    w = wn.window_width()
    print("Height, Width", h, w)
    limit = 20 # Limit for detecting Collision, i.e. Says Collision if distance between two objects is less than limit
    leftwall = -w / 2 + 40
    rightwall = w / 2 - 50

    # Generating all the Pens and moving them to their intial locations
    pens = [turtle.Turtle() for i in range(9)]
    colors = ["white", "white", "white", "white", "yellow", "yellow", "orange", "#E5C453", "black"]
    penspeed = [0, 2, 2, 0, 0, 0, 0, 0, 0]
    move = (score_w, score_h) = (60, 25) # For Adjusting the distance b/w Two entries of Up Table of (v1, v2)
    start = (score_x, score_y) = (-w / 2 + 100, h / 2 - 75) # For Adjusting the Starting Cords of Up Table of (v1, v2)
    intial = [(0, 0), (60, -(h / 2 - 117)), (0, -(h / 2 - 107)), (score_x, score_y), (score_x, score_y - score_h),
              (score_x, score_y - 2 * score_h), (rightwall - limit, -(h / 2 - 150)), (-w / 2 + 200, h / 2 - 50), (0,0)]
    for i in range(0, len(pens)):
        pens[i].up()
        pens[i].pencolor(colors[i])
        pens[i].goto(intial[i][0], intial[i][1])
        pens[i].speed(penspeed[i])
        pens[i].down()

    big = pens[1]
    small = pens[2]
    big.shape("square")
    big.shapesize(2, 2)
    small.shape("square")
    pens[8].shape("square")
    pens[8].shapesize(w/20 + 200, h/20 + 200)
    if not settings["show-path"]:
        big.up()
        small.up()

    if settings["solid"]:
        big.color("white")
        small.color("white")


    # Writing the Title
    pens[7].write("Perfectly Elastic Collision --> m1 = {}kg  m2 = {}kg  u1 = {} m/sec  u2 = {} m/sec \t\tCollision Count = {}".format(data['m1'],data['m2'], data['u1'],data['u2'], data['col']) , font=("Calibri", 15, "bold"))


    # Writing the headings of Up Table
    writer = None
    if settings["show-table-data"]:
        writer = [pens[i] for i in range(3, 6)]
        heading = ["Collisions", "V (m1)", "V (m2)"]
        write_score(writer, heading, move, start, rightwall, heading=True)


    # Loading the Data from Preprocessed File
    a = data['a']
    b = data['b']
    speed = data['data']

    # Drawing the Surface of Wall and Floor
    drawsurface(pens[0], h, w)

    # Drawing the Ellipse For Graph, (cenx, ceny) adjusts the center of ellpise
    cenx = w / 2 - 200
    ceny = 200
    if settings["fitscreen"]:
        (magx, magy) = fitToScreen(data['a'], data['b'], stretch=settings["stretch"])
    else:
        (magx, magy) = (1, 1)

    if settings["show-plot"]:
        drawEllipse(pens[0], a, b, cenx=cenx, ceny=ceny, pen_color="yellow", fitscreen = settings["fitscreen"], stretch= settings["stretch"])
        ellipse_screen(pens[0], cenx, ceny, a * magx, b * magy, 50)
        pens[0].up()
        pens[0].pencolor("white")
        pens[0].goto(cenx + speed[0][0] * magx, ceny + speed[0][1] * magy)
        pens[0].down()

    specs = {'cenx' : cenx, 'ceny' : ceny, 'move' : move, 'start' : start, 'rightwall' : rightwall, 'leftwall' : leftwall,
             'limit' : limit, 'magx' : magx, 'magy' : magy}
    simulate(data, writer, pens, specs, settings)
    pens[0].up()
    pens[0].pencolor("orange")
    pens[0].goto(cenx - a*magx, ceny + b*magy + 25)
    pens[0].down()
    pens[0].write("Then the two blocks never met",font=("Calibri", 15, "bold") )
    if imagefile:
        captureImage(pens[0], imagefile)

    if settings["manual-close"]:
        turtle.done()
    else:
        turtle.Screen().bye()


def draw():
    infile = "Output/Backup/10m50M-10v-5V.json"
    with open(infile, 'r') as fp:
        data = json.load(fp)
    settings = {"show-table-data" : True , "show-plot" : True, "fitscreen" : True, "stretch" : True, "speed-at-last" : False, "show-path" : False, "solid" : True, "manual-close": True}
    starter(data, settings)


if __name__ == "__main__":
    files = ["100m10u.json", "2m10u.json", "1m10u.json", "1000m10u.json"]
    infile = files[0]
    # Loading data
    with open(infile, 'r') as fp:
        data = json.load(fp)
    settings = {"show-table-data" : True , "show-plot" : True, "fitscreen" : True, "stretch" : True, "speed-at-last" : False, "show-path" : False, "solid" : True, "manual-close": True}
    starter(data, settings)
