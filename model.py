from math import sqrt

import numpy as np
import streamlit as st


def h_var_increment(hn, Tp, A, Qdn, B):
    return Tp / A * (Qdn - B * sqrt(hn)) + hn


def u_i():
    return Tp / Ti * sum(uchyb)


def u_d(uchyb):
    return Td / Tp * (uchyb[-1] - uchyb[-2])


def u_pid(uchyb):
    return Kp * (uchyb[-1] + u_i() + u_d(uchyb))


def is_in_range(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def get_Ys(N, Tp, A, Qd, B, u):
    ys = [0, 0]
    for i in range(1, N):
        ys.append(h_var_increment(ys[-1], Tp, A, Qd * u, B))
        uchyby = []
        for j in range(len(ys)):
            uchyby.append(h - ys[j])
        u = is_in_range(u_pid(uchyby), 0.0, 10.0)
    return ys

def get_plot_data(freq):
    Qd = freq * 0.005
    tab = get_Ys(N, Tp, A, Qd, B, freq)
    print("Wartość ustalona poziomu wody: " + str(tab[N]) + " m")

    ypoints = np.array(tab)
    xpoints = np.arange(0, N + 1)

    return [xpoints, ypoints]


h = 5
output = 1
uchyb = [h - output]

Kp = 1
Ti = 10
Td = 0.01
A = 1.5
B = 0.035
Tp = 0.1
tsin = 360
N = int(tsin / Tp)
