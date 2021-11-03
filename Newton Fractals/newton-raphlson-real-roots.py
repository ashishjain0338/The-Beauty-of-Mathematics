from helper import polynomial, roundoff, inputEquation
import numpy as np
if __name__ == '__main__':
    eq = inputEquation()
    l = int(input('Enter the left extreme of range \t-->\t'))
    r = int(input('Enter the right extreme of range \t-->\t'))
    points = int(input('Enter the number of data points to find root in your given range \t --> \t'))
    count = {}

    for x in np.linspace(l, r, points):
        r = roundoff(eq.root(x, 0.1))
        try:
            count[str(r)] = count[str(r)] + 1
        except KeyError:
            count[str(r)] = 1

    print("Roots of ", eq,"--> ", [keys if keys != 'None' else "" for keys in count ])


