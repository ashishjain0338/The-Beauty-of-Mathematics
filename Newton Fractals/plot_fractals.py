import simplejson as json
import matplotlib.pyplot as plt
inputfile = "backup4.json"
outputimage = "500x500(5 Roots)dp.png"
color = {}
cur = 1
re = []
img = []
co = []
cmap = ["#ffffff", "yellow", "purple"]
with open(inputfile, "r") as fp:
    data = json.load(fp)["data"]
    for point in data:
        try:
            re.append(point[0])
            img.append(point[1])
            co.append(color[str(complex(point[2], point[3]))])
        except KeyError:
            color[str(complex(point[2], point[3]))] = cur
            co.append(cur)
            cur = cur + 1


print(len(re), len(img), len(co),cur)
plt.scatter(re, img, c = co, cmap="turbo_r")
plt.savefig(outputimage, bbox_inches='tight')
plt.show()