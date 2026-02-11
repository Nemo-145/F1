import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
# from logging_config import logger as log
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from loader import load_data, load_models, prepare_input 

st.set_page_config(
    page_title= 'F1 pet-project',
    page_icon="📊",
    layout="wide",           
    initial_sidebar_state="auto",)

df = load_data()

drivers = sorted(df['FullName'].unique())
teams = sorted(df['TeamName'].unique())
race = sorted(df['Grand Prix'].unique())
numbers = pd.DataFrame(np.arange(1, 22))
models = ['Random Forest', 'XgBoost', 'CatBoost']
st.sidebar.header('Models')
selected_model = st.sidebar.selectbox('Choose a model', models, index=None, width=200)
st.sidebar.header('Race parameters')
with st.sidebar.form('race form'):
    driver = st.selectbox("Choose a racer", drivers, index=None, width=200)
    team = st.selectbox("Choose a team", teams, index=None, width=200)
    race = st.selectbox("Choose a grand prix", race, index=None, width=200)
    number = st.selectbox("Choose a start position", numbers, index=None, width=200)
    submitted = st.form_submit_button('Make prediction')

if submitted:
    input_data = {
        'FullName': driver,
        'TeamName': team,
        'Grand Prix': race,
        'GridPosition': number,
        'Year': 2026
    }
    model, features = load_models(selected_model)
    if model is not None and features is not None:
        df_prepared = prepare_input(input_data, features, selected_model)
        
        prediction = model.predict(df_prepared)[0]
        
        st.success(f'Finish forecast {prediction:.1f}')

    else:
        st.error('Error loading model')
        # log.error('Error loading model')




