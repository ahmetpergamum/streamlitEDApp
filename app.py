import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('./data/suicides_clean.csv')
st.set_page_config(page_title='Suicide Rates',layout='wide')
st.write('#### Exploratory Data Analysis(EDA) for Suicide Rates')

continuous = [col for col in df.columns if df[col].dtype!='object']
categoric = [col for col in df.columns if df[col].dtype=='object']

sidebar_select_ops = st.sidebar.selectbox(
    "Select the type of anaysis.",
    ("Dataframe", "Univariate-continuous", "Univariate-categoric", 'World map'),
    index=3
)

if sidebar_select_ops=='Dataframe':
    st.write('Dataframe exploration')
    op_country = st.sidebar.selectbox('Select the country.', (df.country.unique()))
    op_year = st.sidebar.selectbox('Select the year.', (df[df.country==op_country].year.unique()))
    st.write(df[(df.country==op_country)&(df.year==op_year)])
elif sidebar_select_ops=='Univariate-continuous': 
    st.write('Univariate Analysis of Continuous Variables')
    op_cont = st.sidebar.selectbox('Select the variable.', (continuous))
    fig, ax = plt.subplots(figsize=(20,6))
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
elif sidebar_select_ops=='World map': 
    df_agg = df.groupby(['country','year']).agg(suicide_sum=('suicides_no','sum'), 
                                       suicide_100k_pop=('suicides_100k_pop','sum'),
                                       population=('population','sum'),
                                       region=('region','first'), sub_region=('sub_region','first'),
                                       gdp=('gdp','first'),
                                       gdp_per_capita=('gdp_per_capita','first'),
                                       iso_alpha=('iso_alpha','first'),
                                      )
    df_agg = df_agg.reset_index()
    df_agg = df_agg.sort_values(by=['year','country'])
    years = list(df_agg.year.unique())
    op_year = st.sidebar.selectbox('Select the year.', (years),index=years.index(2015) )
    op_color = st.sidebar.selectbox('Select the color.', ('gdp_per_capita','region','sub_region','gdp'))
    op_size = st.sidebar.selectbox('Select the size.', ('suicide_100k_pop','suicide_sum'))
    st.write('World map for year '+str(op_year))

    fig = px.scatter_geo(df_agg[df_agg.year==op_year], locations="iso_alpha", color=op_color,
                         hover_name="country", size=op_size,
                         hover_data={'suicide_sum': True,"suicide_100k_pop": ":.2f",
                             "population": True, "gdp_per_capita": True, "iso_alpha": False},
                         #projection="orthographic"
                         )
    fig.update_layout( width=800, height=800, hoverlabel_align = 'right' )
    st.plotly_chart(fig, use_container_width=True)
