import pandas as pd
import plotly.express as px
import streamlit as st

import model
import slider_helper as sh

st.sidebar.button('Refresh')
compare_mode = st.sidebar.checkbox('Compare mode')


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
    df = pd.DataFrame(dict(x=data[0], y=data[1]))
    fig = px.line(df, x="x", y=["y"], color_discrete_map={"y": "red"})
    update_layout_plot(fig, "x", "y", False)
    st.write(fig)


def two_plots_and_write(data1, data2):
    df = pd.DataFrame(dict(x=data1[0], Original=data1[1], Compare=data2[1]))
    fig = px.line(df, x="x", y=["Original", "Compare"],
                  color_discrete_map={"Original": "red", "Compare": "blue"})

    update_layout_plot(fig, "x", "y", True)
    st.write(fig)


def draw_in_compare_mode():
    original_slider_column, compared_slider_column = st.columns(2)
    freeze_original = st.sidebar.checkbox('Freeze original')

    with original_slider_column:
        st.error("Original")
        kp = set_sliders(sh.SLIDER_NAME_KP, 2.0, freeze_original)
        kd = set_sliders(sh.SLIDER_NAME_KD, 1.4, freeze_original)
        ki = set_sliders(sh.SLIDER_NAME_KI, 1.4, freeze_original)

    with compared_slider_column:
        st.info("Compare")
        compared_variables = sh.get_variables_for_compared()
        compared_kp = set_sliders(sh.SLIDER_NAME_KP, compared_variables[0], False, True)
        compared_kd = set_sliders(sh.SLIDER_NAME_KD, compared_variables[1], False, True)
        compared_ki = set_sliders(sh.SLIDER_NAME_KI, compared_variables[2], False, True)

    two_plots_and_write(get_data_for_draw(kp, kd, ki), get_data_for_draw(compared_kp, compared_kd, compared_ki))


def draw_in_normal_mode():
    kp = set_sliders(sh.SLIDER_NAME_KP, 2.0)
    kd = set_sliders(sh.SLIDER_NAME_KD, 1.4)
    ki = set_sliders(sh.SLIDER_NAME_KI, 1.4)
    sh.set_states_variables([kp, kd, ki])
    plot_and_write(get_data_for_draw(kp, kd, ki))


def get_data_for_draw(kp, kd, ki):
    return model.get_plot_data(kp, kd, ki)


def draw():
    if compare_mode:
        draw_in_compare_mode()
    else:
        draw_in_normal_mode()


draw()
