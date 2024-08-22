import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import poisson

my_lambda = 20

c = 4
print("Pr(X=%g)="%c, +(poisson.pmf(c,my_lambda)))
print("Pr(X<=%g)="%c,+(poisson.cdf(c,my_lambda)))
mean, var, skew, kurt = poisson.stats(my_lambda, moments='mvsk')
print("mean=",mean,"\t std=", np.sqrt(var))

x_list = np.linspace(0, my_lambda*3, my_lambda*3+1)
y = poisson.pmf(x_list,my_lambda)
cdf = poisson.cdf(x_list,my_lambda)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
plt.subplot(1, 2, 1)
plt.bar(x_list, y)
plt.xlabel('x')
plt.ylabel('pmf')
plt.title('X~poisson(%g)'%my_lambda)

plt.subplot(1, 2, 2)
plt.step(x_list, cdf)
plt.xlabel('x')
plt.ylabel('cdf')
plt.title('X~poisson(%g)'%my_lambda)
fig.tight_layout()

