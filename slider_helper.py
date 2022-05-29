import streamlit as st

SLIDER_NAME_KP = "Kp"
SLIDER_NAME_KD = "Kd"
SLIDER_NAME_KI = "Ki"

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


def get_variables_for_compared():
    compared_kp = get_variable_for_slider(SLIDER_NAME_KP)
    compared_kd = get_variable_for_slider(SLIDER_NAME_KD)
    compared_ki = get_variable_for_slider(SLIDER_NAME_KI)
    return [compared_kp, compared_kd, compared_ki]


def set_states_variables(values):
    dicts = {SLIDER_NAME_KP: values[0], SLIDER_NAME_KD: values[1], SLIDER_NAME_KI: values[2]}
    st.experimental_set_query_params(**dicts)


def values_for_sliders():
    return {
        SLIDER_NAME_KP: {
            SLIDER_STEP_VALUE: 0.1,
            SLIDER_MIN_VALUE: 0.0,
            SLIDER_MAX_VALUE: 5.0
        },
        SLIDER_NAME_KD: {
            SLIDER_STEP_VALUE: 0.1,
            SLIDER_MIN_VALUE: 0.0,
            SLIDER_MAX_VALUE: 5.0
        },
        SLIDER_NAME_KI: {
            SLIDER_STEP_VALUE: 0.1,
            SLIDER_MIN_VALUE: 0.0,
            SLIDER_MAX_VALUE: 5.0
        }
    }


