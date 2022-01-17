from codecs import ignore_errors
import time

import altair as alt
import pandas as pd
import streamlit as st

from controllers import Controller

# Main
st.title('Virus Spread Simulation')

CHART_WIDTH = 600
CHART_HEIGHT = 600

# Sidebar # TODO: Add help to controls

st.sidebar.title('Parameters')
pop_num = st.sidebar.slider('Population size', 10, 1000, 100)
map_size_x = st.sidebar.slider('Map size x', 10, 200, 100)
map_size_y = st.sidebar.slider('Map size y', 10, 200, 100)
init_infected = st.sidebar.slider('Initialy infected people', 1, 20, 1)
infection_dist = st.sidebar.slider('Infection distance', 1, 20, 10)
infection_prob = st.sidebar.slider('Infection probability', 0., 1., 0.5)
death_probability = st.sidebar.slider('Death probability', 0., 1., 0.05)
walking_range = st.sidebar.slider('Walking range', 0., 10., 2.)
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
        color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
    ).properties(width=CHART_WIDTH + 200, height=CHART_HEIGHT - 200)

if 'cont' not in st.session_state:
    st.session_state.cont = cont

if 'df' not in st.session_state:
    st.session_state.df = df

if 'base_chart' not in st.session_state:
    st.session_state.base_chart = base_chart


def plot_animation(df):
    chart = alt.Chart(df).mark_line().encode(
        x='step:Q',
        y='number of people:Q',
        color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
    ).properties(width=CHART_WIDTH, height=CHART_HEIGHT)

    return chart    

def simulate(controller, steps):
    # current_step = controller.step_number
    controller = st.session_state.cont
    line_plot = st.session_state.line_plot
    df = st.session_state.df
    current_step = controller.step_number
    controller.simulate(steps)
    for idx in range(current_step, controller.step_number + 1):
        new_df = pd.DataFrame({'step': [], 'number of people': [], 'health status': []})
        for status in range(5):
            print(idx, len(controller.stats[str(status)]))
            new_df = new_df.append(pd.Series({'step': idx, 'number of people': controller.stats[str(status)][idx-1], 'health status': str(status)}), ignore_index=True)
        line_plot.add_rows(new_df)
    st.session_state.cont = controller
    st.session_state.line_plot = line_plot
    st.session_state.df = df

line_plot = st.altair_chart(base_chart)

stacked_area_chart = alt.Chart(df).mark_area().encode(
    x='step:Q',
    y=alt.Y('number of people:Q', stack='normalize'),
    color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
).properties(width=CHART_WIDTH + 200, height=CHART_HEIGHT - 200)    
stacked_area_chart_st = st.altair_chart(stacked_area_chart)


donut_placeholder = st.empty()
donut_chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
    theta='number of people:Q',
    color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
).properties(width=CHART_WIDTH, height=CHART_HEIGHT)  

donut_placeholder.altair_chart(donut_chart)
positions = pd.DataFrame({'pos_x': cont.stats['pos_x'][-1], 'pos_y': cont.stats['pos_y'][-1], 'health status': cont.stats['status'][-1]})
positions_placeholder = st.empty()
positions_chart = alt.Chart(positions).mark_point().encode(
    x='pos_x:Q',
    y='pos_y:Q',
    color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
).properties(width=CHART_WIDTH, height=CHART_HEIGHT)
positions_placeholder.altair_chart(positions_chart)

col1, col2, col3 = st.columns(3)

with col1:
    steps = st.number_input('Number of steps', 10, 1000, 100)
with col2:
    st.write('#')
    start = st.button('Start')#, on_click=simulate, args=(cont, steps, ))
with col3:
    st.write('#')
    reset = st.button('Reset')

if start:
    controller = st.session_state.cont
    df = st.session_state.df
    current_step = controller.step_number
    controller.simulate(steps)
    for idx in range(current_step, controller.step_number + 1):
        new_df = pd.DataFrame({'step': [], 'number of people': [], 'health status': []})
        positions_data = pd.DataFrame({'pos_x': controller.stats['pos_x'][idx-1], 'pos_y': controller.stats['pos_y'][idx-1], 'health status': [str(stat) for stat in controller.stats['status'][idx-1]]})
        for status in range(5):
            new_df = new_df.append(pd.Series({'step': idx, 'number of people': controller.stats[str(status)][idx-1], 'health status': str(status)}), ignore_index=True)
        line_plot.add_rows(new_df)
        stacked_area_chart_st.add_rows(new_df)
        donut_chart = alt.Chart(new_df).mark_arc(innerRadius=50).encode(
            theta='number of people:Q',
            color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
        ).properties(width=CHART_WIDTH, height=CHART_HEIGHT)
        donut_placeholder.altair_chart(donut_chart)

        positions_chart = alt.Chart(positions_data).mark_point().encode(
            x='pos_x:Q',
            y='pos_y:Q',
            color=alt.Color('health status:O', scale=alt.Scale(domain=['0', '1', '2', '3', '4'], range=['#5ad45a', '#e6d800', '#b30000', '#1a53ff', '#000000'])) 
        ).properties(width=CHART_WIDTH, height=CHART_HEIGHT)
        positions_placeholder.altair_chart(positions_chart)        
    st.session_state.cont = controller
    st.session_state.df = df

