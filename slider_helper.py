import streamlit as st

SLIDER_NAME_FREQUENCY = "Frequency"
SLIDER_NAME_ANOTHER = "Another"

SLIDER_MIN_VALUE = "min_value"
SLIDER_MAX_VALUE = "max_value"
SLIDER_STEP_VALUE = "step_value"


def get_states_variables(variable, default):
    app_state = st.experimental_get_query_params()
    return app_state[variable][0] if variable in st.experimental_get_query_params() else default


def get_mid_value_of_slide(slider_name):
    return (values_for_sliders()[slider_name][SLIDER_MIN_VALUE] +
            values_for_sliders()[slider_name][SLIDER_MAX_VALUE]) / 2


def get_variable_for_slider(name):
    return float(get_states_variables(name, str(get_mid_value_of_slide(name))))


def get_variables_for_frozen():
    freeze_freq = get_variable_for_slider(SLIDER_NAME_FREQUENCY)
    freeze_another = get_variable_for_slider(SLIDER_NAME_ANOTHER)
    return [freeze_freq, freeze_another]


def set_states_variables(values):
    dicts = {SLIDER_NAME_FREQUENCY: values[0], SLIDER_NAME_ANOTHER: values[1]}
    st.experimental_set_query_params(**dicts)


def values_for_sliders():
    return {
        SLIDER_NAME_FREQUENCY: {
            SLIDER_STEP_VALUE: 0.1,
            SLIDER_MIN_VALUE: 0.0,
            SLIDER_MAX_VALUE: 10.0
        },
        SLIDER_NAME_ANOTHER: {
            SLIDER_STEP_VALUE: 0.1,
            SLIDER_MIN_VALUE: 0.0,
            SLIDER_MAX_VALUE: 10.0
        }
    }


