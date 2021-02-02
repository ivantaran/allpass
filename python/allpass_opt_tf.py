
from scipy import signal
from matplotlib import pyplot
import numpy as np
from scipy import constants


def init(n=3):
    ft = 100.0e6
    dt = 1.0 / ft
    lam = constants.c * dt

    # dref = np.array([
    #     109.0, 92.0, 76.0, 59.0, 45.0, 32.0, 23.0, 14.0, 10.0, 7.5, 7.0, 6.0, 9.5, 15.0
    # ])
    dref = np.array([
        6.0, 9.0, 11.0, 15.0, 22.5, 27.5, 34.0, 38.0, 39.5, 41.0, 46.0, 57.5, 78.0, 110.0
    ])
    dref = dref * 0.2 / 19.0 / lam * 360.0 / 180.0 * 1.0

    np.random.seed()
    a = np.random.randn(n)
    b = np.random.randn(1)
    wsys = np.arange(24.0e6 % 562500.0, 50.0e6, 562500.0) * np.pi * 2.0 * dt
    p = {}
    p['ft'] = ft
    p['dt'] = dt
    p['lam'] = lam
    return a, b, wsys, dref, p


def a2sys(a, dt):
    a: np.ndarray
    n = a.shape[0]
    p = np.array(a, dtype='complex')
    for i in range(0, n, 2):
        if a[i] < a[i + 1]:
            delta = (a[i + 1] - a[i]) * 0.5
            p[i] = np.complex(a[i], delta)
            p[i + 1] = np.complex(a[i], -delta)
    den = np.poly(p)
    num = np.flip(den)
    sys = signal.TransferFunction(num, den, dt=dt)
    return sys


def jacobian(wsys, a, b, dt, delta):
    n = a.shape[0]
    m = wsys.shape[0]
    jac = np.empty((n + 1, m))
    for i in range(n):
        a0 = np.array(a)
        a0[i] -= delta[i]
        sys0 = a2sys(a0, dt)
        a1 = np.array(a)
        a1[i] += delta[i]
        sys1 = a2sys(a1, dt)
        y0 = fx(wsys, sys0, b)
        y1 = fx(wsys, sys1, b)
        jac[i] = 0.5 * (y1 - y0) / delta[i]
    jac[n] = np.ones(m)
    return jac


def cost(wsys, sys: signal.TransferFunction, b, dref):
    e = error(wsys, sys, b, dref)
    return np.sum(np.square(e)) / dref.shape[0]


def fx(wsys, sys: signal.TransferFunction, b, normalize=True):
    _, _, phase = sys.bode(w=wsys)
    if normalize:
        phase = (phase - 180.0) / 180.0
    y = np.gradient(phase) + b
    # y = phase + b
    return y


def error(wsys, sys: signal.TransferFunction, b, dref, n=35):
    e = np.zeros(wsys.shape[0])
    y = fx(wsys, sys, b)[n:n + dref.shape[0]]
    e[n:n + dref.shape[0]] = y + dref
    return e


# def tune_delta(wsys, sys, b):
#     epsilon0 = 1.0e-5
#     n = sys.num.shape[0]
#     m = wsys.shape[0]
#     delta = np.ones(n - 1)
#     while True:
#         delta0 = delta / (1.0 + 10.0 * np.random.random(n - 1))
#         jac = jacobian(wsys, sys, b, delta)[:-1]
#         jac0 = jacobian(wsys, sys, b, delta0)[:-1]
#         djac = np.abs(jac - jac0)
#         idx = djac > epsilon0
#         idx = np.sum(idx, axis=1) > 0.0
#         if np.any(idx):
#             delta[idx] = delta0[idx]
#         else:
#             break
#     return delta


n = 6
a, b, wsys, dref, p = init(n)
sys = a2sys(a, p['dt'])

lam = 0.001
# delta = tune_delta(wsys, sys, b)
delta = np.ones(n) * 1.0e-9
cc = []
sigma = 1.0e0

pyplot.ion()
fig, ax = pyplot.subplots(2, 2)
fig.set_size_inches(16, 9)
ax0 = ax[0, 0]
ax1 = ax[0, 1]
ax2 = ax[1, 0]
ax3 = ax[1, 1]
circle = pyplot.Circle((0, 0), 1.0, fill=False)

w, _, _ = sys.bode(w=wsys)
w = w * 0.5 / np.pi
n = 35
SCALE = 1.0e1
f0 = w[n:dref.shape[0] + n]
cmin = 1.0e10
c = 20.0
c0 = 0.0
batch_size = 1000
i = 0
lam0 = 1.0e-3  # 7.03181e-12
ok = True
# delta = tune_delta(wsys, sys, b)
identity = np.identity(sys.num.shape[0])
while True:
    jac = jacobian(wsys, a, b, sys.dt, delta)
    h = np.matmul(jac, jac.transpose())
    # hinv = np.linalg.pinv(h)
    # hinv = np.linalg.pinv(lam0 * np.identity(sys.num.shape[0]))
    hinv = np.linalg.pinv(h + lam0 * identity * h + identity * 1.0)
    e = np.reshape(error(wsys, sys, b, dref), (wsys.shape[0], 1))
    da = np.matmul(hinv, jac)
    da = np.matmul(da, e)
    a0 = np.array(a)
    a0 -= np.squeeze(da[:-1]) * sigma
    b0 = b - da[-1] * sigma
    sys0 = a2sys(a0, sys.dt)
    c = c0
    c0 = cost(wsys, sys0, b0, dref)

    # b = b0
    # sys = sys0
    # cmin = c0

    if c0 < cmin:
        b = b0
        a = a0
        sys = sys0
        cmin = c0
        # lam0 /= 1.0 + np.random.random() * 5.0
        lam0 /= 5.0
    elif c0 < c:
        pass
        # lam0 /= 1.01
        # lam0 /= 1.0 + np.random.random() * 5.0
    else:
        lam0 *= 1.5
    if lam0 < 1.0e-20 or lam0 > 1.0e20:
        lam0 = 1.0e-20

    cc.append(c0)
    if (i % batch_size) == 0:
        # delta = tune_delta(wsys, sys, b)
        y = fx(wsys, sys, b)
        # print(c)
        ax: pyplot.Axes
        ax0.cla()
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax0.grid()
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax0.plot(f0, dref, '-o', alpha=0.5)
        ax0.set_xlim([0, 50.0e6])
        ax0.plot(w, -y, '-o', alpha=0.5)
        ax0.plot(w, e, '-o')
        # ax2.plot(f0, np.gradient(dref))
        # ax2.plot(w, np.gradient(-y))
        ax1.set_xlim([0, batch_size])
        ax1.plot(np.log10(cc) * 10.0, 'o-')

        ax3.scatter(np.real(sys.poles), np.imag(sys.poles))
        ax3.set_xlim([-1.5, 1.5])
        ax3.set_ylim([-1.5, 1.5])
        ax3.add_patch(circle)

        fig.canvas.draw()
        fig.canvas.flush_events()
        cc.clear()
    if (i % batch_size) == 0:
        print(sys.num)
        print(b)
        print('%g' % lam0)
        print(cmin)
    i += 1

print(sys)
print(b)
# exit(0)

pyplot.ioff()
pyplot.show()
