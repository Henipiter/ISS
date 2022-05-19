import streamlit as st
from matplotlib import pyplot as plt
import model
import pandas as pd
import numpy as np


def get_states_variables(variable, default):
    app_state = st.experimental_get_query_params()
    return app_state[variable][0] if variable in st.experimental_get_query_params() else default


compare_mode = st.sidebar.checkbox('Compare mode')
plot_bool = st.sidebar.checkbox('Plot')


def plot_and_write(data, color='ro'):
    if (plot_bool):
        fig = plt.figure()
        plt.plot(data[0], data[1], color)
        st.write(fig)
    else:
        chart_data = pd.DataFrame(data[1], index=data[0])
        st.line_chart(chart_data, use_container_width=True)


def two_plots_and_write(data1, data2, color1='ro', color2='bo'):
    if (plot_bool):
        fig = plt.figure()
        plt.plot(data1[0], data1[1], color1)
        plt.plot(data2[0], data2[1], color2)
        st.write(fig)
    else:
        chart_data = pd.DataFrame(list(zip(data1[1], data2[1])), index=data1[0])
        st.line_chart(chart_data, use_container_width=True)


def draw_in_compare_mode():
    original_slider_column, both_plots_column, compared_slider_column = st.columns([1, 3, 1])
    freeze_original = st.sidebar.checkbox('Freeze original')

    with original_slider_column:
        freq = st.slider('Frequency [V]', 0.0, 10.0, 5.0, step=0.1, disabled=freeze_original)
        another = st.slider('Another', 0.0, 10.0, 5.0, step=0.1, disabled=freeze_original)

        st.error("Original")

    with compared_slider_column:
        freeze_freq = get_states_variables("Frequency [V]", "0.5")
        freeze_another = get_states_variables("Another", "0.5")
        freeze_freq = st.slider(label="freeze_freq", value=float(freeze_freq), step=0.1, min_value=0.0, max_value=10.0)
        freeze_another = st.slider(label="freeze_another", value=float(freeze_another), step=0.1, min_value=0.0,
                                   max_value=10.0)

        st.info("Compared")
    with both_plots_column:
        two_plots_and_write(model.get_plot_data(freq), model.get_plot_data(float(freeze_freq)))

    original_plot_column, compared_plot_column = st.columns(2)
    with original_plot_column:
        plot_and_write(model.get_plot_data(freq), 'ro')
    with compared_plot_column:
        plot_and_write(model.get_plot_data(float(freeze_freq)), 'bo')


def draw_in_normal_mode():
    freq = st.sidebar.slider('Frequency [V]', 0.0, 10.0, 5.0, step=0.1)
    another = st.sidebar.slider('Antorhe', 0.0, 10.0, 5.0, step=0.1)
    st.experimental_set_query_params(another=another, freq=freq)

    st.header("Actual")
    plot_and_write(model.get_plot_data(freq), 'ro')


def draw():
    if compare_mode:
        draw_in_compare_mode()

    else:
        draw_in_normal_mode()


draw()
