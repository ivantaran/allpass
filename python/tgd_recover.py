from matplotlib import pyplot
from scipy import constants
from scipy import signal
import numpy as np


def envelope(x, rate=1.0):
    a = np.abs(np.sinc(rate * x) * rate)
    return a


def tgda(x):
    p = np.array([1, 2, 1]) * 0.1
    g = np.polyval(p, x)
    return g


n = 100
xc = np.linspace(-4.0, 4.0, num=n)
x0 = np.linspace(0.0, 8.0, num=n)
x1 = np.linspace(-8.0, 0.0, num=n)
x = np.linspace(x0, x1, num=n)
a = envelope(x)
g = np.reshape(tgda(x0), (1, -1))

ax0: pyplot.Axes
ax0 = pyplot.subplot()
ax0.grid()
# ax0.plot(xc, a, 'tab:blue', alpha=0.3)
# ax0.plot(x0, a, 'tab:blue', alpha=0.3)

ax0.plot(xc, np.squeeze(g), 'tab:red')
ax0.plot(xc, np.sum(a * g, axis=0) / n, 'tab:blue')
ax0.plot(xc, np.squeeze(a[n//2]), 'tab:orange')
# ax0.plot(xc, np.squeeze(a[-1]), 'tab:orange')
pyplot.show()
