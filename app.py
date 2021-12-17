import streamlit as st


# Main
st.title('Virus Spread Simulation')

st.sidebar.title('Parameters')
num_pop = st.sidebar.slider('Population size', 10, 1000, 100)
map_size_x = st.sidebar.slider('Map size x', 10, 200, 100)
map_size_y = st.sidebar.slider('Map size y', 10, 200, 100)
init_infected = st.sidebar.slider('Initialy infected people', 1, 20, 1)
infection_dist = st.sidebar.slider('Infection distance', 1, 20, 10)
infection_prob = st.sidebar.slider('Infection probability', 0., 1., 0.5)
death_probability = st.sidebar.slider('Death probability', 0., 1., 0.05)
walking_range = st.sidebar.slider('Walking range', 0., 1., 0.1)
incubation_period = st.sidebar.slider('Incubation period', 0, 5, 3)
illness_period = st.sidebar.slider('Illness period', 1, 20, 10)
lockdown = st.sidebar.checkbox('Lockdown', value=False)
lockdown_range = st.sidebar.slider('Lockdown steps range', 1, 1000, (50, 150)) # TODO: Check for max steps
self_isolation = st.sidebar.checkbox('Self isolation', value=False)
