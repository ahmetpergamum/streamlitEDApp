import streamlit as st
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./data/suicide_clean.csv')

# st.set_page_config(layout='wide')
# st.title('Exploratory Data Analysis(EDA) for Suicide Rates')
st.write('#### Exploratory Data Analysis(EDA) for Suicide Rates')

# st.markdown('How are **the suicide rates** affected?')

continuous = [col for col in df.columns if df[col].dtype!='object']
categoric = [col for col in df.columns if df[col].dtype=='object']

sidebar_select_ops = st.sidebar.selectbox(
    "Select the type of anaysis.",
    ("Dataframe", "Univariate-continuous", "Univariate-categoric")
)


if sidebar_select_ops=='Dataframe':
    st.write('Dataframe exploration')
    op_country = st.sidebar.selectbox('Select the country.', (df.country.unique()))
    op_year = st.sidebar.selectbox('Select the year.', (df[df.country==op_country].year.unique()))
    st.write(df[(df.country==op_country)&(df.year==op_year)])
elif sidebar_select_ops=='Univariate-continuous': 
    st.write('Univariate Analysis of Continuous Variables')
    op_cont = st.sidebar.selectbox('Select the variable.', (continuous))
    fig, ax = plt.subplots()
    ax = sns.distplot(df[op_cont], kde=False)
    ax.set(title='Histogram of ' + op_cont)
    st.pyplot(fig)

elif sidebar_select_ops=='Univariate-categoric': 
    st.write('Univariate Analysis of Categoric Variables')
    op_cat = st.sidebar.selectbox('Select the variable.', (categoric))
    fig, ax = plt.subplots(figsize=(20,6))
    ax = sns.countplot(df[op_cat])
    ax.tick_params(axis="x", rotation=90)
    ax.set(title='Countplot of ' + op_cat)
    st.pyplot(fig)


# st.balloons()
