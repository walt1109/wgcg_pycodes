import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import geom

p = 1/100

c = 8
print("Pr(X=%g)="%c, +(geom.pmf(c,p)))
print("Pr(X<=%g)="%c,+(geom.cdf(c,p)))
mean, var, skew, kurt = geom.stats(p, moments='mvsk')
print("mean=",mean,"\t std=", np.sqrt(var))

x_list = np.linspace(1, 1000, 1000)
y = geom.pmf(x_list,p)
cdf = geom.cdf(x_list,p)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
plt.subplot(1, 2, 1)
plt.bar(x_list, y)
plt.xlabel('x')
plt.ylabel('pmf')
plt.title('X~geom(%g)'%p)

plt.subplot(1, 2, 2)
plt.step(x_list, cdf)
plt.xlabel('x')
plt.ylabel('cdf')
plt.title('X~geom(%g)'%p)
fig.tight_layout()

