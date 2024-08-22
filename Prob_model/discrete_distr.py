import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import randint

a = 81
b = 100
#DiscUnif in {a, a+1, ..., b}
#Python randint takes "a" and "b+1" as parameters

c = 90
print("Pr(X=%g)="%c, +(randint.pmf(c,a,b+1)))
print("Pr(X<=%g)="%c,+(randint.cdf(c,a,b+1)))
mean, var, skew, kurt = randint.stats(a, b+1, moments='mvsk')
print("mean=",mean,"\t std=", np.sqrt(var))

x_list = np.linspace(a, b, b-a+1)
#generate x = a,a+1,..,b so that we can calculate p(x) = Pr(X=x)
y = randint.pmf(x_list,a,b+1)
#pmf for DiscreteUnif(a,b) at x=a, a+1, ..., b
cdf = randint.cdf(x_list,a,b+1)
#cdf for DiscreteUnif(a,b) at x=a, a+1, ..., b

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
plt.subplot(1, 2, 1)
plt.bar(x_list, y)
plt.xlabel('x')
plt.ylabel('pmf')
plt.title('X~DiscUnif(%g,'%a+' %g)'%b)

plt.subplot(1, 2, 2)
plt.step(x_list, cdf)
plt.xlabel('x')
plt.ylabel('cdf')
plt.title('X~DiscUnif(%g,'%a+' %g)'%b)
fig.tight_layout()

