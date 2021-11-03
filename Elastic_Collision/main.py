import simplejson as json
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from animate import starter

def getPoints(m1, m2 , u1 = 0, u2 = -1,stop = 1000, outfile = None ):
    col = 0
    s = m1*u1**2 + m2*u2**2
    a = (s/m2)**0.5
    b = (s/m1)**0.5
    output = {'m1' : m1, 'm2' : m2, 'u1' : u1, 'u2' : u2 ,'col_type' : "Perfectly Elastic" ,'a' : a, 'b' : b,'col' :0,'data' : [(u2, u1)]}
    if((u1 < 0 and u2 > 0) or (u1 < 0 and u2 < 0 and abs(u1) >= abs(u2))):
        output['data'].append((u2, -u1))
        col = col + 1
        u1 = -u1
        output['col'] = 1
    if (u1 >= 0 and u2 >= 0 and u2 >= u1):
        return output

    while True:
        if(stop == 0):
            print("Preventing Infinte Loop , Increase the stop factor")
            break
        stop = stop - 1
        # A) Collision within the blocks
        s = m1 + m2
        v1 = ((m1 - m2)/s)*u1 + (2*m2/s)*u2
        v2 = (2*m1/s)*u1 + ((m2 - m1)/s)*u2
        col = col + 1
        output['data'].append((v2, v1))
        # print("Col ", col, " --> ", v1, v2)
        if (v1 >= 0 and v2 >= 0 and v2 >= v1):
            break

        # B) Collision with the Wall
        u1 = -v1
        u2 = v2
        col = col + 1
        output['data'].append((u2, u1))
        # print("Col ", col, " --> ",u1, u2)
        if (u1 >= 0 and u2 >= 0 and u2 >= u1):
            break

    output['col'] = col
    print("Number of Collsions --> ", col)

    if(outfile != None):
        with open(outfile, 'w') as fp:
            json.dump(output, fp, indent=4)
    return output

def graph(data, imagefile = None):
    y = [coord[1] for coord in data['data']]
    x = [coord[0] for coord in data['data']]
    (a, b) = (data['a'], data['b'])

    t = np.linspace(0, 2 * pi, 100)
    plt.plot(a * np.cos(t), b * np.sin(t), 'k--')
    plt.grid(color='lightgray', linestyle='dashed')

    plt.plot(x, y)
    plt.title("Perfectly Elastic Collision \nm1 = {}kg  m2 = {}kg  u1 = {} m/sec  u2 = {} m/sec Collision Count = {}".format(data['m1'],data['m2'], data['u1'],data['u2'], data['col']) + "\nPlot of v2 V/s v1")
    plt.xlabel("V2")
    plt.ylabel("V1")
    if(imagefile):
        plt.savefig(imagefile, bbox_inches='tight')
    # plt.grid(color='lightgray',linestyle='--')
    plt.show()

if __name__  == "__main__":
    m1 = 1
    m2 = 1000
    u1 = 0
    u2 = -10
    with open("settings.json", "r") as fp:
        settings = json.load(fp)
    data = getPoints(m1, m2, u1, u2)
    TESTING = False
    if TESTING:
        filename = "{}m{}M{}v{}V".format(m1,m2,u1,u2)
        with open("Output/Backup/" + filename + ".json", "w") as fp:
            json.dump(data, fp, indent=4)
        print("Backup Created at ", filename)
        graph(data, "Output/Images/" + filename + "G.png")
        starter(data, settings, "Output/Images/" + filename + "A")
    else:

        choice = 1
        while choice != 4:
            choice = int(input("Make Your Selection :\n 1) Take Backup of Calculated Data\n 2) Generate Plot\n 3) Visualise using animations\n 4) Exit\n -->"))
            if choice == 1:
                filename = input('Enter the name of backup file you wish to make: ')
                filename = "/Output/Backup/" + filename + ".json"
                with open(filename, "w") as fp:
                    json.dump(data, fp, indent = 4)
                print("Backup Created at ", filename)
            elif choice == 2:
                save = input('If you wish to save the plot as image, Then enter image name, else enter N :')
                if(not (save == "N" or save == "n")):
                    filename = "Output/Images/" + save + ".png"
                    graph(data, filename)
                    print("Image saved at ", filename)
                else:
                    graph(data)
            elif choice == 3:
                save = input('If you wish to save the animation as image, Then enter image name, else enter N or n :')
                if (not (save == "N" or save == "n")):
                    filename = "Output/Images/" + save
                    starter(data, settings, filename)
                    print("Image saved at ", filename)
                else:
                    starter(data, settings)

            else:
                break
