
from scipy import signal
from matplotlib import pyplot
import numpy as np
from scipy import constants

# a = np.array([1.11215064, -0.57602822,  2.07481254, -0.46176302,  1.])
a = np.array([-0.07610893, -0.03128678,  0.90923851, -0.6250264,   1., ])
# a = np.array([0.843941,   -0.92055061,  2.08364254, -1.00716152,  1., ])
scale = 2.0**13  # / np.max(np.abs(a))
c = np.round(a * scale)
print(c)
# a = c
ft = 100.0e6
dt = 1.0 / ft
lam = constants.c * dt
wsys = np.arange(24.0e6 % 562500.0, 50.0e6, 562500.0) * np.pi * 2.0 * dt
sys: signal.TransferFunction
sys = signal.TransferFunction(a, np.flip(a), dt=dt)
w, mag, phase = signal.dbode(sys, w=wsys)
t, y = signal.dimpulse(sys, n=100)
ax1 = pyplot.subplot(212)
ax3 = pyplot.subplot(221)
print(sys)
print('poles', sys.poles)
print('abs poles', np.abs(sys.poles))
ax2 = ax1.twinx()
ax2_ = ax1.twinx()
ax1.plot(w, mag, 'tab:red')
ax2.plot(w, phase, 'tab:blue')
ax2_.plot(w, np.gradient(phase), 'tab:orange')
ax1.set_ylim([-1.0, 1.0])
ax4 = pyplot.subplot(222)
ax4: pyplot.Axes
circle = pyplot.Circle((0, 0), 1.0, fill=False)
ax4.scatter(np.real(sys.poles), np.imag(sys.poles))
ax4.set_xlim([-1.5, 1.5])
ax4.set_ylim([-1.5, 1.5])
ax4.add_patch(circle)
ax4.grid()
# ax3.plot(t * 1.0e9, 20.0 * np.log10(np.abs(np.squeeze(y))))
ax3.step(t * 1.0e9, np.squeeze(y), '-')
ax1.grid()
ax3.grid()
pyplot.show()
