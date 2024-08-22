import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import uniform

#Unif(10,20)
a = 10
b = 20

c = 16
print("Pr(X<=%g)="%c,+(uniform.cdf(c,a,b-a)))
mean, var, skew, kurt = uniform.stats(a,b-a, moments='mvsk')
print("mean=",mean,"\t std=", np.sqrt(var))

x_list = np.linspace(1, 30, 100)
y = uniform.pdf(x_list,a,b-a)
cdf = uniform.cdf(x_list,a,b-a)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
plt.subplot(1, 2, 1)
plt.plot(x_list, y)
plt.xlabel('x')
plt.ylabel('pdf')
plt.title('X~Unif(%g,'%a+'%g)'%b)

plt.subplot(1, 2, 2)
plt.plot(x_list, cdf)
plt.xlabel('x')
plt.ylabel('cdf')
plt.title('X~Unif(%g,'%a+'%g)'%b)
fig.tight_layout()

