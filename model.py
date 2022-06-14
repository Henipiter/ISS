from math import sqrt
import simpful as sf

import numpy as np


def h_var_increment(hn, Tp, A, Qdn, B):
    return Tp / A * (Qdn - B * sqrt(hn)) + hn


def h_var_increment2(y1, y2, y3, u1, u2, u3, a1, a2, a3, b1, b2, b3):
    return a1 * y1 + a2 * y2 + a3 * y3 + b1 * u1 + b2 * u2 + b3 * u3

def u_i(Ki):
    return Ki * sum(uchyb)


def u_d(uchyb, Kd):
    return Kd * (uchyb[-1] - uchyb[-2])


def u_pid(uchyb, Kp, Ki, Kd):
    return Kp * uchyb[-1] + u_i(Ki) + u_d(uchyb, Kd)


def is_in_range(value, min_val, max_val):
    return max(min(value, max_val), min_val)


def get_Ys_pid(N, Tp, a1, a2, a3, b1, b2, b3, Kp, Ki, Kd):
    ys = [0, 0, 0]
    u = [0, 0, 0]
    for i in range(1, N):
        ys.append(h_var_increment2(ys[-1], ys[-2], ys[-3], u[-1], u[-2], u[-3], a1, a2, a3, b1, b2, b3))
        uchyby = []
        for j in range(len(ys)):
            uchyby.append(h - ys[j])
        u.append(is_in_range(u_pid(uchyby, Kp, Ki, Kd), -1.0, 1.0))
    return ys


def setup_fuzzy():
    FS = sf.FuzzySystem()

    # Define a linguistic variable.
    S_1 = sf.FuzzySet(points=[[-5., 1.], [0., 0.], [5., 0.]], term="low_flow")
    S_2 = sf.FuzzySet(points=[[-5., 0], [-1., 0], [0., 1.], [1., 0.], [5., 0]], term="medium_flow")
    S_3 = sf.FuzzySet(points=[[-5., 0], [0., 0.], [5., 1.]], term="high_flow")
    FS.add_linguistic_variable("OXI", sf.LinguisticVariable([S_1, S_2, S_3]))

    # Define consequents.
    FS.set_crisp_output_value("LOW_POWER", -1)
    FS.set_crisp_output_value("MEDIUM_POWER", 0)
    FS.set_crisp_output_value("HIGH_POWER", 1)
    FS.set_output_function("HIGH_FUN", "OXI**2")

    # Define fuzzy rules.
    RULE1 = "IF (OXI IS low_flow) THEN (POWER IS LOW_POWER)"
    RULE2 = "IF (OXI IS medium_flow) THEN (POWER IS MEDIUM_POWER)"
    RULE3 = "IF (OXI IS high_flow) THEN (POWER IS HIGH_POWER)"
    # RULE4 = "IF (NOT (OXI IS low_flow)) THEN (POWER IS HIGH_FUN)"
    FS.add_rules([RULE1, RULE2, RULE3])

    return FS
    # Set antecedents values, perform Sugeno inference and print output values.


def calculate_fuzzy(FS, uchyb):
    FS.set_variable("OXI", uchyb)
    return FS.Sugeno_inference(['POWER'])["POWER"]


def get_Ys_fuzzy(N, Tp, a1, a2, a3, b1, b2, b3):
    ys = [0., 0., 0.]
    u = [0., 0., 0.]
    FS = setup_fuzzy()
    for iiiiii in range(1, N):
        ys.append(h_var_increment2(ys[-1], ys[-2], ys[-3], u[-1], u[-2], u[-3], a1, a2, a3, b1, b2, b3))
        uchyby = []
        for j in range(len(ys)):
            uchyby.append(h - ys[j])
            u.append(calculate_fuzzy(FS, uchyby[j]))
    return ys


def get_plot_data(kp, kd, ki):
    Kp = kp
    Kd = kd
    Ki = ki

    # tab = get_Ys_pid(N, Tp, a1, a2, a3, b1, b2, b3, Kp, Ki, Kd)
    tab = get_Ys_fuzzy(N, Tp, a1, a2, a3, b1, b2, b3)

    print("Wartość ustalona wychylenia: " + str(tab[N]) + " rad")

    ypoints = np.array(tab)
    xpoints = np.arange(0, N + 2)

    return [xpoints, ypoints]


h = 2.0
output = 1
uchyb = [h - output]

Kp = 1.9758
Ki = 0.0115
Kd = 1.4008

# Ti = 10
# Td = 0.01
# A = 1.5
# B = 0.035
Tp = 0.1
tsin = 50
N = int(tsin / Tp)

a1 = 2.571
a2 = -2.151
a3 = 0.5798
b1 = 0.001062
b2 = 0.003726
b3 = 0.000809
