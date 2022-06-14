import pandas as pd
import plotly.express as px
import streamlit as st

import model
import slider_helper as sh

invert_plots = False
st.sidebar.button('Refresh')
fuzzy_mode = st.sidebar.checkbox('Fuzzy')

if not fuzzy_mode:
    compare_mode = st.sidebar.checkbox('Compare mode')
else:
    compare_mode = False


def get_y_of_ustalona(length):
    y = []
    for i in range(length):
        y.append(2)
    return y


def set_sliders(name, current_value, disabled=False, compared=False):
    i = sh.values_for_sliders()[name]
    label = name + " compared" if compared else name
    min_value = i[sh.SLIDER_MIN_VALUE]
    max_value = i[sh.SLIDER_MAX_VALUE]
    step = i[sh.SLIDER_STEP_VALUE]
    current = current_value if min_value <= current_value <= max_value else (min_value + max_value) / 2
    return st.slider(label=label, value=current, step=step,
                     min_value=min_value, max_value=max_value, disabled=disabled)


def update_layout_plot(fig, xaxis_title, yaxis_title, showlegend):
    fig.update_layout(
        showlegend=showlegend,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=""
    )
    fig.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)", )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#555555')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#555555')


def plot_and_write(data):
    z = get_y_of_ustalona(len(data[0]))
    df = pd.DataFrame(dict(x=data[0], y=data[1], Zadana=z))
    fig = px.line(df, x="x", y=["Zadana", "y"], color_discrete_map={"Zadana": "yellow", "y": "red"})

    update_layout_plot(fig, "x", "y", False)
    st.write(fig)
    st.write("Wartość ustalona: ", data[1][-1])
    st.write("Tp:", 0.1)


def two_plots_and_write(data1, data2):
    global invert_plots
    invert_plots = st.sidebar.checkbox('Invert plots')
    z = get_y_of_ustalona(len(data1[0]))
    df = pd.DataFrame(dict(x=data1[0], Original=data1[1], Compare=data2[1], Zadana=z))
    y = ["Zadana", "Original", "Compare"] if invert_plots else ["Zadana", "Compare", "Original"]
    fig = px.line(df, x="x", y=y,
                  color_discrete_map={"Original": "red", "Compare": "blue", "Zadana": "yellow"})

    update_layout_plot(fig, "x", "y", True)
    st.write(fig)


def draw_in_compare_mode():
    original_slider_column, compared_slider_column = st.columns(2)
    freeze_original = st.sidebar.checkbox('Freeze original')

    with original_slider_column:
        st.error("Original")
        kp = set_sliders(sh.SLIDER_NAME_KP, 0.5, freeze_original)
        kd = set_sliders(sh.SLIDER_NAME_KD, 1.7, freeze_original)
        ki = set_sliders(sh.SLIDER_NAME_KI, 0.08, freeze_original)

    with compared_slider_column:
        st.info("Compare")
        compared_variables = sh.get_variables_for_compared()
        compared_kp = set_sliders(sh.SLIDER_NAME_KP, compared_variables[0], False, True)
        compared_kd = set_sliders(sh.SLIDER_NAME_KD, compared_variables[1], False, True)
        compared_ki = set_sliders(sh.SLIDER_NAME_KI, compared_variables[2], False, True)
    ori_data = get_data_for_draw(kp, kd, ki)
    compared_data = get_data_for_draw(compared_kp, compared_kd, compared_ki)
    two_plots_and_write(ori_data, compared_data)

    with original_slider_column:
        st.write("Wartosc ustalona: ", ori_data[1][-1])
        st.write("Tp:", 0.1)
    with compared_slider_column:
        st.write("Wartosc ustalona: ", compared_data[1][-1])
        st.write("Tp:", 0.1)


def draw_in_normal_mode():
    if not fuzzy_mode:
        kp = set_sliders(sh.SLIDER_NAME_KP, 0.5)
        kd = set_sliders(sh.SLIDER_NAME_KD, 1.7)
        ki = set_sliders(sh.SLIDER_NAME_KI, 0.08)
        sh.set_states_variables([kp, kd, ki])
    else:
        kp = 0
        kd = 0
        ki = 0
    plot_and_write(get_data_for_draw(kp, kd, ki))


def get_data_for_draw(kp, kd, ki):
    return model.get_plot_data(kp, kd, ki, fuzzy_mode)


def draw():
    if compare_mode:
        draw_in_compare_mode()
    else:
        draw_in_normal_mode()


draw()
