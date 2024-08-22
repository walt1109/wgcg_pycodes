import numpy as np
from scipy import integrate
from mpmath import nsum

#integrate 5x^4 from 1 to 3
f = lambda x: 5* x**4
ans,err = integrate.quad(f, 1, 4) #integrate f from 1 to 4; it returns answer for the integral and error.
print(ans)

#integrate (1/3) * x * e^(-1/3 * x) from 0 to infinity
f = lambda x: 1/3 * x * np.exp(-1/3 * x)
ans,err = integrate.quad(f, 0, np.inf)
print(ans)

#integrate (x-2) * 0.5 * e^(-0.5 * x) from x = 2 to infinity
f = lambda x: (x-2)* 0.5 * np.exp(-0.5 * x)
ans,err = integrate.quad(f, 2, np.inf)
print(ans)

#integrate int_0^2 int_0^x 2xy dy dx
f = lambda y, x: 2*x*y  # y is inner and x is outer integral
ans,err = integrate.dblquad(f, 0, 2, lambda x: 0, lambda x: x)
#give a range of outer (i.e., x) first and then a range of inner (i.e., y)
#which can be a function of outer variable, x
print(ans)

#integrate int_0^infinity int_0^infinity e^(-(x+2y)) dy dx
f = lambda y, x: np.exp(-(x+2*y))  # y is inner and x is outer integral
ans,err = integrate.dblquad(f, 0, np.inf, 0, np.inf)
#give a range of outer (i.e., x) first and then a range of inner (i.e., y)
#which can be a function of outer variable, x
print(ans)

#sum (99/100)^n from n = 1 to infinity
f = nsum(lambda n: (99/100)**n, [1,np.inf])
print(f)
