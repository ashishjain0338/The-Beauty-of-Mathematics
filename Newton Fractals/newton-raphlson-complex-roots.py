from helper import polynomial, complexRoundOff, inputEquation
import numpy as np
import simplejson as json
outfile = "backup4.json"
if __name__ == "__main__":
    eq = polynomial(5, [complex(-2.5,5.4), complex(3.8,0.5),5.5, 3, 4], 2)
    r = eq.root(complex(10,20), 0.1)
    print(eq)
    l = -10
    r = 10
    points = 500
    count = {}
    data_points = np.linspace(l, r, points)
    # print(data_points)
    backup = {"eq" : str(eq), "roots" : {}, "data" : []}
    for x in data_points:
        for y in data_points:
            num = complex(x, y)
            r = complexRoundOff(eq.root(num, 0.1))
            try:
                backup["data"].append((num.real, num.imag, r.real, r.imag))
            except:
                pass
            # print(num, " --> ", r)
            try:
                count[str(r)] = count[str(r)] + 1
            except KeyError:
                count[str(r)] = 1
    backup["roots"] = count
    with open(outfile, 'w') as fp:
        json.dump(backup, fp, indent=4)
    print(count)