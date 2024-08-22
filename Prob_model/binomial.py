import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import binom

trials = 6
p = 1/2

c = 9
print("Pr(X=%g)="%c, +(binom.pmf(c,trials,p)))
print("Pr(X<=%g)="%c,+(binom.cdf(c,trials,p)))
print("Pr(X>%g)="%c, +(1 - binom.cdf(c,trials,p)))
mean, var, skew, kurt = binom.stats(trials, p, moments='mvsk')
print("mean=",mean,"\t std=", np.sqrt(var))

x_list = np.linspace(1, trials, trials)
#generate x = 1,2,..,n so that we can calculate p(x) = Pr(X=x)
y = binom.pmf(x_list,trials,p, loc=0)
#pmf for Bin(30,0.9) at x=1,2,...,30
cdf = binom.cdf(x_list, trials, p)
#cdf for Bin(30,0.9) at x=1,2,...,30

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
plt.subplot(1, 2, 1)
plt.bar(x_list, y)
plt.xlabel('x')
plt.ylabel('pmf')
plt.title('X~Binomial(%g,'%trials+' %g)'%p)

plt.subplot(1, 2, 2)
plt.step(x_list, cdf)
plt.xlabel('x')
plt.ylabel('cdf')
plt.title('X~Binomial(%g,'%trials+' %g)'%p)
fig.tight_layout()
