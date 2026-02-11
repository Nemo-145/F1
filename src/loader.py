import streamlit as st
import pandas as pd
import joblib
import os
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from logging_config import logger as log
import sys

@st.cache_resource
def load_models(model: str):
    if model == 'CatBoost':
        model_name = 'catboost_model_v1.cbm'
        features_name = 'catboost_features_v1.pkl'
    elif model == 'Random Forest':
        model_name = 'rf_model_v1.pkl'
        features_name = 'rf_features_v1.pkl'
    elif model == 'XgBoost':
        model_name = 'xgboost_model_v1.pkl'
        features_name = 'xgboost_features_v1.pkl'
    else:
        log.error('What the hell did you pass on???') # It will need to be changed
        return None, None
    model_path = os.path.join("models", model_name)
    features_path = os.path.join("models", features_name)
    try:
        if model == 'Random Forest':
            model_loaded = joblib.load(model_path)
            features_loaded = joblib.load(features_path)
        elif model == 'XgBoost':
            model_loaded = joblib.load(model_path)
            features_loaded = joblib.load(features_path)
        elif model == 'CatBoost':
            model_loaded = CatBoostRegressor()
            model_loaded.load_model(model_path)
            features_loaded = joblib.load(features_path)
    except FileNotFoundError:
        log.error('Model or features is mot found')
        return None, None
    
    return model_loaded, features_loaded

@st.cache_data
def load_data():
    try:
        csv_path = os.path.join('data', 'raw', 'all_races_2022_2025.csv')
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        log.error('Model or features is not found')
        return None
    return df

def prepare_input(input_data, feature_list, model_type):
    df_input = pd.DataFrame([input_data])
    if model_type == 'CatBoost':
        df_input = df_input.reindex(columns=feature_list, fill_value=0)
    elif model_type in ['Random Forest', 'XgBoost']:
        df_input = pd.get_dummies(df_input, columns = ['TeamName'], drop_first=False, prefix='Team')
        df_input = pd.get_dummies(df_input, columns = ['Grand Prix'], drop_first=False, prefix='GP')
        df_input = pd.get_dummies(df_input, columns = ['FullName'], drop_first=False)
        bools_cols = df_input.select_dtypes(include=['bool']).columns
        df_input[bools_cols] = df_input[bools_cols].astype('int64')
        df_input.replace({True: 1, False: 0}, inplace=True)
        df_input = df_input.reindex(columns=feature_list, fill_value=0)
    else:
        log.error('Incorrect model')
        return None
    return df_input