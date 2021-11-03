# from math import round
class polynomial:
    '''
        Polynomial refers to the form a(d) * x^d + a(d - 1)*x^(d - 1) + ________ + a1*x + a0
        where ad, a1, a0 are the coefficients/contents of coeff and d is degree of polynomial
        Method 1 or None represents the default method of defining the polynomial using coefficients
        Method 2 represents defining the polynomial by providing the root location.
        '''
    def __init__(self, degree, coef, method = None):
        self.degree = degree
        self.derivative = None
        if(method == 2):
            self.coef = self.eqFromRoots(coef)
        else:
            self.coef = coef


    def eqFromRoots(self ,roots):
        c = [1]
        for r in roots:
            r = -r
            out = c[:]
            out.append(0)
            index = 1
            for val in c:
                out[index] = out[index] + val * r
                index = index + 1
            c = out[:]
        return  c

    def create_derivative(self):
        '''It finds out the derivative of our polynomial eq'''
        coeff = [self.coef[self.degree - d]*d for d in range(self.degree, 0, -1)]
        self.derivative =  polynomial(self.degree - 1, coeff)
        print(self.derivative)

    def eval(self, x):
        out = 0
        for c in self.coef:
            out = out*x + c
        return out

    def d_eval(self, x):
        if(self.derivative == None):
            self.create_derivative()
        return self.derivative.eval(x)

    def root(self, start, precision):
        r = start
        for counter in range(0, 20):
            fx = self.eval(r)
            if (abs(fx) < precision):
                return r
            else:
                try:
                    r = r - fx / self.d_eval(r)
                except ZeroDivisionError:
                    pass
                except Exception as e:
                    print("Eror in step size:", e)
        return None


    def __str__(self):
        poly = ""
        for i in range(0, self.degree + 1):
            if(not(self.coef[i] == 1 or self.coef[i] == 0) or (self.coef[i] == 1 and i == self.degree)):
                poly = poly + str(self.coef[i])
            if (i != self.degree and self.coef[i] != 0):
                poly = poly + "x^" + str(self.degree - i) + " + "
            elif(self.coef[i] == 0):
                pass
            else:
                poly = poly + " = 0"

        return poly

def roundoff(val):
    if(val == None):
        return val
    if(abs(val - round(val)) <= 0.1):
        return round(val)
    else:
        return round(val,1)

def complexRoundOff(num):
    if (num == None):
        return num
    return complex(roundoff(num.real), roundoff(num.imag))


def inputEquation():
    degree = int(input('Enter the degree of polynomial\t:'))
    choice = int(input("There lies two option to define the polynomial \n 1) Entering Coefficeints \n 2) Entering roots\n Make Your selection :"))
    coef = []
    if(choice == 1):
        for i in range(degree, -1, -1):
            coef.append(int(input('Enter the coefficient of x^' + str(i) + '\t:')))
        eq = polynomial(degree, coef)
    else:
        for i in range(1, degree + 1):
            coef.append(int(input('Enter root Number ' + str(i) + ' \t:')))
        eq = polynomial(degree, coef, 2)
    print("Entered Polynomial Equation is :", eq)


if __name__ == '__main__':
    eq = polynomial(2, [1,1,1])
    # eq = eqFromRoots([1.54,2.65,-9.18])
    print(eq)
    count = {}
    for x1 in range(-2000,2000):
        x = x1/2
        r = roundoff(root(eq, x, 0.1))
        try:
            count[str(r)] = count[str(r)] + 1
        except KeyError:
            count[str(r)] = 1
        # print(x, " --> ", roundoff(root(eq, x, 0.1)))

    print(count)