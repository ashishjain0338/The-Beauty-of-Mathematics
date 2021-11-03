from draw import *
import simplejson as json


def analyse(data, degree):
    x = 0
    y = 0
    turn = 1
    maxy = 0
    line = [0, 0, 0, 0]
    for i in range(0, len(data)):
        if(i != 0):
            if(data[i] != data[i - 1]):
                turn = turn + 1
        if(data[i] == 0):
            y = y + 1
        elif(data[i] == 2):
            y = y - 1
        elif (data[i] == 1):
            x = x + 1
        else:
            x = x - 1
        line[data[i]] = line[data[i]] + 1
        maxy = max(maxy, y)
    return {'Degree': degree, 'Lines': len(data), 'Turns': turn, 'X-span': x, 'Y-span': y,
         'Max-Y-Reach': maxy, 'line-type' : line}

output = [{'Degree' : 'General d', 'Lines' : '2^(2*d) - 1', 'Turns' : ' If Odd --> 4*(Previous Turns) - 1, If Even --> 4*(Previous Turns) + 1 ','X-span': '2^d - 1', 'Y-span': 0, 'Max-Y-Reach' : '2^d - 1',
           'line-type' : ['Vertical Up (2^(2*d - 2))', 'Horizontal Right (2^(d - 1)*(2^(d - 1) + 1) - 1)', 'Vertical Down (2^(2*d - 2))', 'Horizontal Left (2^(d - 1)*(2^(d - 1) - 1))']}]
def analyseCurve(n):
    '''It is a recursive fxn that generates the next stage of hilbert curve
        cell --> (n - 1) degree Psuedo Hilbert Curve,This fxn would analyse
        1) Number of unit lines
        2) Number of Turns
        3) X-span distance
        4) Y-span distance
        5) Area filled with defined width ()
        '''
    if n == 1:
        output.append(analyse([0,1,2], n))
        return [0, 1, 2]


    current = analyseCurve(n - 1)

    out = shift90(current[:])
    out.append(0)
    out.extend(current)
    out.append(1)
    out.extend(current)
    out.append(2)
    out.extend(shift270(current[:]))
    print("Degree done --> ", n)
    output.append(analyse(out, n))
    return out

analyseCurve(13)
with open('analysis.json', 'w') as fp:
    json.dump(output, fp, indent=4)
print(output)