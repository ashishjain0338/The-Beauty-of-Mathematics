import turtle
import numpy as np
import simplejson as json

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lerp(self, p2, t):
        return p2*t + self*(1 - t)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if(type(other) != Point):
            return Point(self.x*other, self.y*other)
        else:

            return Point(self.x*other.x, self.y*other.y)

    def __str__(self):
        return " ({},{}) ".format(self.x, self.y)

def write(writer, cp,h, w):
    writer.up()
    writer.goto(-100, h/2 - 60)
    writer.write('{} Degree Bezier Curve'.format(len(cp) - 1),font=("Calibri", 25, "bold"))
    writer.goto(-w/2 +50, h/2 -100)
    string = ""
    for i in range(0, len(cp)):
        string += "P" + str(i) + str(cp[i]) + "\t"
    print(string)
    writer.write( string, font=("Calibri", 15, "bold"))
    # exit()

def starter():
    '''Setting up the Screen to Full Screen'''
    global wn
    wn = turtle.Screen()
    wn.setup(width=1.0, height=1.0)  # For Fullscreen
    wn.title("Collide")
    h = wn.window_height()
    w = wn.window_width()
    back = turtle.Turtle()
    back.color("#0F1825")
    back.shape("square")
    back.shapesize(w / 20 + 200, h / 20 + 200)


def animate(cp,settings ,magx = 1, magy = 1):
    cp = [Point(p.x*magx, p.y*magy) for p in cp]
    h = wn.window_height()
    w = wn.window_width()
    lines = len(cp) - 1
    extra = 3

    # Counting the number of pens according to the degree
    if settings["show-only-curve"]:
        pen_count = extra + 1
    elif(settings["show-only-main"]):
        pen_count = lines + extra + 1
    else:
        pen_count = lines*(lines + 1)//2 + extra

    # Generating all the Pens and moving them to their intial locations
    pens = [turtle.Turtle() for i in range(pen_count)]
    colors = ["black", "white", "yellow"]
    penspeed = [0, 2, 0]
    penspeed.extend([0 for i in range(int(pen_count) - extra)])
    loc = []
    for i in range(lines, 0, -1):
        for j in range(i):
            try:
                colors.append(settings["colors"][str(i)])
            except:
                print("Increase the number of colors in settings file, Currently using default --> Pink")
                colors.append("pink")
            loc.append((cp[j].x, cp[j].y))


    intial = [(0, 0), (cp[0].x, cp[0].y), (cp[0].x, cp[0].y)]
    intial.extend(loc)
    for i in range(0, len(pens)):
        pens[i].up()
        pens[i].pencolor(colors[i])
        pens[i].goto(intial[i][0], intial[i][1])
        pens[i].speed(penspeed[i])
        pens[i].down()
        pens[i].pensize(2)

    # Drawing the Control Points
    pens[1].pensize(1)
    pens[1].fillcolor("white")
    pens[1].begin_fill()
    pens[1].circle(5)
    pens[1].end_fill()
    write(pens[2], cp, h, w)
    if settings["show-only-curve"]:
        pens[1].up()

    for i in range(1, len(cp)):
        pens[1].goto(cp[i].x, cp[i].y)
        pens[1].begin_fill()
        pens[1].circle(5)
        pens[1].end_fill()


    # Drawing the required Bezier Curve
    t_space = np.linspace(0, 1 , 100)
    for t in t_space:
        next = [cp[i].lerp(cp[i + 1],  t) for i in range(lines)]
        online = next
        if settings["show-only-main"] or settings["show-only-curve"]:
            while(len(next) != 1):
                next = [next[i].lerp(next[i + 1], t) for i in range(0, len(next) - 1)]
            if not settings["show-only-curve"]:
                for i in range(0, len(online)):
                    pens[i + extra].goto(online[i].x, online[i].y)
            pens[len(pens) - 1].goto(next[0].x, next[0].y)
        else:
            for index in range(lines - 1, 0, -1):
                start = len(next) - index - 1
                next.extend([next[start + i].lerp(next[start + i + 1], t) for i in range(0, index)])
            for i in range(extra, pen_count):
                pens[i].goto(next[i - extra].x, next[i - extra].y)

    turtle.done()

# test1 = [Point(4,5), Point(200,150), Point(100, -250), Point(-100,0), Point(200, -150), Point(-100, -300)]
# test_y = [Point(4,-5), Point(200,-150), Point(100, 250), Point(-100,0), Point(200, 150), Point(-100, 300)]
# test_x = [Point(-4,5), Point(-200,150), Point(-100, -250), Point(100,0), Point(-200, -150), Point(100, -300)]
# test_xy = [Point(-4,-5), Point(-200,-150), Point(-100, 250), Point(100,0), Point(-200, 150), Point(100, 300)]
# # test = [Point(-300, -300), Point(-50,-50),Point(-300, 300),Point(-50,50), Point(300, 300), Point(50,50), Point(300, -300), Point(50,-50), Point(-300, -300)]
# test = [Point(0,-300), Point(150,150),Point(0,0)]
# print(test)
# settings = {"show-only-main" :  True, "show-only-curve" : True, "colors" :
#     {"1" : "white", "2" : "#461B33" , "3" : "#274E66", "4" : "#38DEA7", "5" : "#7F2D25", "6" : "#FFE056", "7" : "#2995CB", "8" : "pink"}}
# starter()
# animate(test1, settings)
# animate(test_y, settings)
# animate(test_x,settings)
# animate(test_xy, settings)
# turtle.done()

if __name__ == "__main__":
    choice = int(input(' 1) For Manually input the points\n 2) For Taking Input Directly from input.json file\n 3) To '
                       'Regenerate input.json file (if corrupted) \n 4) For Regenerating settings.json file (if corrupted)\n Make Your Selection\t :'))
    if choice == 1:
        with open("settings.json") as fp:
            settings = json.load(fp)
        point_count = int(input("Enter the number of points \t:"))
        cp = []
        for i in range(point_count):
            x = int(input("Enter P{}'s X coordinate\t:".format(i)))
            y = int(input("Enter P{}'s Y coordinate\t:".format(i)))
            cp.append(Point(x, y))
        starter()
        animate(cp, settings)


    elif choice == 2:
        with open("settings.json") as fp:
            settings = json.load(fp)
        with open("input.json") as fp:
            data = json.load(fp)

        cp = [Point(d[0], d[1]) for d in data["points"]]
        starter()
        animate(cp, settings)
    elif choice == 3:
        data = {"point_count" : 6, "points" : [(4,5), (200, 150), (100, -250), (-100, 0), (200, -150), (-100, -300)]}
        with open("input.json", "w") as fp:
            json.dump(data, fp, indent = 4)
        print("Input File Regenerated Successfully")
    elif choice == 4:
        settings = {"show-only-main": True, "show-only-curve": True, "colors":
        {"1" : "white", "2" : "#461B33" , "3" : "#274E66", "4" : "#38DEA7", "5" : "#7F2D25", "6" : "#FFE056", "7" : "#2995CB", "8" : "pink"}}
        with open("settings.json", "w") as fp:
            json.dump(settings, fp, indent=4)
        print("Settings File Regenerated Successfully")
