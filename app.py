import time

import altair as alt
import pandas as pd
import streamlit as st

from controllers import Controller

# Main
st.title('Virus Spread Simulation')


# Sidebar # TODO: Add help to controls

st.sidebar.title('Parameters')
pop_num = st.sidebar.slider('Population size', 10, 1000, 100)
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

params = dict(pop_num=pop_num, map_size=(map_size_x, map_size_y), init_infected=init_infected, infection_dist=infection_dist, infection_prob=infection_prob,
                    death_prob=death_probability, walking_range=(-walking_range, walking_range), incubation_period=incubation_period,
                    illness_period=illness_period)

if lockdown:
    params['lockdown'] = lockdown_range



cont = Controller(**params)


df = pd.DataFrame({'step': [], 'number of people': [], 'health status': []})

base_chart = alt.Chart(df).mark_line().encode(
    x='step:Q',
    y='number of people:Q',
    color='health status:O'
).properties(width=600, height=300)

chart_plot = st.altair_chart(base_chart)

def plot_animation(df):
    chart = alt.Chart(df).mark_line().encode(
        x='step:Q',
        y='number of people:Q',
        color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
    ).properties(width=600, height=300)

    return chart    


def plot(controller, steps, chart_plot):
    df = pd.DataFrame({'step': [], 'number of people': [], 'health status': []})
    controller.simulate(steps)
    for idx in range(1, cont.step_number + 1):
        for status in range(5):
            df = df.append({'step': idx, 'number of people': cont.stats[str(status)][idx-1], 'health status': str(status)}, ignore_index=True)
    for i in range(1, cont.step_number):
        chart = plot_animation(df.loc[df['step'] <= i+1])
        chart_plot = chart_plot.altair_chart(chart)
        time.sleep(0.05)


steps = st.number_input('Number of steps', 10, 1000, 100)

start = st.button('Start', on_click=plot, args=(cont, steps, chart_plot, ))
