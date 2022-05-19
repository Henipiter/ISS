import streamlit as st
from matplotlib import pyplot as plt

import model


def get_states_variables(variable, default):
    app_state = st.experimental_get_query_params()
    return app_state[variable][0] if variable in st.experimental_get_query_params() else default


compare_mode = st.sidebar.checkbox('Compare mode')


def plot_and_write(data, color='ro'):
    fig = plt.figure()
    plt.plot(data[0], data[1], color)
    st.write(fig)


def two_plots_and_write(data1, data2, color1='ro', color2='bo'):
    fig = plt.figure()
    plt.plot(data1[0], data1[1], color1)
    plt.plot(data2[0], data2[1], color2)
    st.write(fig)


def draw_in_compare_mode():
    col1, col2 = st.columns(2)
    freeze_original = st.sidebar.checkbox('Freeze original')

    with col1:
        st.header("Actual")
        freq = st.slider('Frequency [V]', 0.0, 10.0, 5.0, step=0.1, disabled=freeze_original)
        another = st.slider('Antorhe', 0.0, 10.0, 5.0, step=0.1, disabled=freeze_original)

        with st.expander("See original"):
            plot_and_write(model.get_plot_data(freq), 'ro')
    with col2:
        st.header("Freezed")

        freeze_freq = get_states_variables("freq", "0.5")
        freeze_another = get_states_variables("another", "0.5")
        freeze_freq = st.slider(label="freeze_freq", value=float(freeze_freq), step=0.1, min_value=0.0, max_value=10.0)
        freeze_another = st.slider(label="freeze_another", value=float(freeze_another), step=0.1, min_value=0.0,
                                   max_value=10.0)
        with st.expander("See compare"):
            plot_and_write(model.get_plot_data(float(freeze_freq)), 'bo')

    with st.expander("See combined"):
        two_plots_and_write(model.get_plot_data(freq), model.get_plot_data(float(freeze_freq)))


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
