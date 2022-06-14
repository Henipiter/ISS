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
    SET_P_1 = sf.FuzzySet(points=[[-5., 1.], [0., 0.], [5., 0.]], term="low_flow")
    SET_P_2 = sf.FuzzySet(points=[[-5., 0], [-1., 0], [0., 1.], [1., 0.], [5., 0]], term="medium_flow")
    SET_P_3 = sf.FuzzySet(points=[[-5., 0], [0., 0.], [5., 1.]], term="high_flow")
    FS.add_linguistic_variable("P_REG", sf.LinguisticVariable([SET_P_1, SET_P_2, SET_P_3]))

    SET_D_1 = sf.FuzzySet(points=[[-5., 1.], [0., 0.], [5., 0.]], term="low_flow")
    SET_D_2 = sf.FuzzySet(points=[[-5., 0], [-0.5, 0], [0., 1.], [0.5, 0.], [5., 0]], term="medium_flow")
    SET_D_3 = sf.FuzzySet(points=[[-5., 0], [0., 0.], [5., 1.]], term="high_flow")
    FS.add_linguistic_variable("D_REG", sf.LinguisticVariable([SET_D_1, SET_D_2, SET_D_3]))

    # Define consequents.
    FS.set_crisp_output_value("POWER_0", -1)
    FS.set_crisp_output_value("POWER_1", -0.5)
    FS.set_crisp_output_value("POWER_2", 0)

    FS.set_crisp_output_value("POWER_3", 0.5)
    FS.set_crisp_output_value("POWER_4", 1)

    # Define fuzzy rules.
    RULE_P1 = "IF (P_REG IS low_flow) AND (D_REG IS low_flow) THEN (POWER IS POWER_0)"
    RULE_P2 = "IF (P_REG IS low_flow) AND (D_REG IS medium_flow) THEN (POWER IS POWER_1)"
    RULE_P3 = "IF (P_REG IS medium_flow) AND (D_REG IS medium_flow) THEN (POWER IS POWER_2)"
    RULE_P4 = "IF (P_REG IS high_flow) AND (D_REG IS medium_flow) THEN (POWER IS POWER_3)"
    RULE_P5 = "IF (P_REG IS high_flow) AND (D_REG IS high_flow) THEN (POWER IS POWER_4)"
    FS.add_rules([RULE_P1, RULE_P2, RULE_P3, RULE_P4, RULE_P5])
    return FS


def calculate_fuzzy(FS, uchyb, roznica):
    FS.set_variable("P_REG", uchyb)
    FS.set_variable("D_REG", roznica)
    return FS.Sugeno_inference(['POWER'])["POWER"]


def get_Ys_fuzzy(N, Tp, a1, a2, a3, b1, b2, b3):
    ys = [0., 0., 0.]
    u = [0., 0., 0.]
    FS = setup_fuzzy()
    for iiiiii in range(1, N):
        print("[", str(iiiiii), "/" + str(N) + "]")
        ys.append(h_var_increment2(ys[-1], ys[-2], ys[-3], u[-1], u[-2], u[-3], a1, a2, a3, b1, b2, b3))
        uchyby = []
        for j in range(len(ys)):
            uchyby.append(h - ys[j])
        for j in range(len(ys)):
            u.append(calculate_fuzzy(FS, uchyby[j], uchyby[j] - uchyby[j - 1]))
    return ys


def get_plot_data(kp, kd, ki, is_fuzzy):

    if is_fuzzy:
        tab = get_Ys_fuzzy(N, Tp, a1, a2, a3, b1, b2, b3)
    else:
        Kp = kp
        Kd = kd
        Ki = ki
        tab = get_Ys_pid(N, Tp, a1, a2, a3, b1, b2, b3, Kp, Ki, Kd)

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
tsin = 90
N = int(tsin / Tp)

a1 = 2.571
a2 = -2.151
a3 = 0.5798
b1 = 0.001062
b2 = 0.003726
b3 = 0.000809
