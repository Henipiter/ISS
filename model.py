from math import sqrt

import numpy as np


def h_var_increment(hn, Tp, A, Qdn, B):
    return Tp / A * (Qdn - B * sqrt(hn)) + hn


def h_var_increment2(y1,y2,y3,u1,u2,u3,a1,a2,a3,b1,b2,b3):
    return a1*y1 + a2*y2 + a3*y3 + b1*u1 + b2*u2 + b3*u3

def u_i(Ki):
    return Ki * sum(uchyb)


def u_d(uchyb, Kd):
    return Kd * (uchyb[-1] - uchyb[-2])


def u_pid(uchyb, Kp, Ki, Kd):
    return Kp * uchyb[-1] + u_i(Ki) + u_d(uchyb,Kd)


def is_in_range(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def get_Ys(N, Tp, a1, a2, a3, b1, b2, b3, Kp, Ki, Kd):
    ys = [0, 0, 0]
    u = [0, 0, 0]
    for i in range(1, N):
        #ys.append(h_var_increment(ys[-1], Tp, A, Qd * u, B))
        ys.append(h_var_increment2(ys[-1], ys[-2], ys[-3], u[-1], u[-2], u[-3], a1, a2, a3, b1, b2, b3))
        uchyby = []
        for j in range(len(ys)):
            uchyby.append(h - ys[j])
        u.append(is_in_range(u_pid(uchyby, Kp, Ki, Kd), -1.0, 1.0))
    return ys

def get_plot_data(kp,kd, ki):
    Kp = kp
    Kd = kd
    tab = get_Ys(N, Tp, a1, a2, a3, b1, b2, b3, Kp, Ki, Kd)
    print("Wartość ustalona wychylenia: " + str(tab[N]) + " rad")

    ypoints = np.array(tab)
    xpoints = np.arange(0, N + 2)

    return [xpoints, ypoints]


h = 2
output = 1
uchyb = [h - output]

Kp = 1.9758
Ki = 0.0115
Kd = 1.4008

#Ti = 10
#Td = 0.01
#A = 1.5
#B = 0.035
Tp = 0.1
tsin = 360
N = int(tsin / Tp)

a1 = 2.571
a2 = -2.151
a3 = 0.5798
b1 = 0.001062
b2 = 0.003726
b3 = 0.000809
