import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#create a header
st.header('Used Car Sales Data')
st.write('Filter the data of used car sales in the US by manufacturer')

#read in the data and create a pandas dataframe
vehicles = pd.read_csv('vehicles_us.csv')

#fill in missing values in the dataset
vehicles['paint_color'] = vehicles['paint_color'].fillna('unknown')
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)
vehicles['odometer'] = vehicles['odometer'].fillna(vehicles['odometer'].mean()).astype('int')
vehicles['cylinders'] = vehicles['cylinders'].fillna(0)
vehicles = vehicles.dropna()

#add a column for manufacturers
vehicles['manufacturer'] = [x.split()[0] for x in vehicles['model']]
manufacturer = vehicles['manufacturer'].unique()


selected_menu = st.selectbox('Select a manufacturer', manufacturer)


#find minimum and maximum values for our slider of model years
min_year, max_year = int(vehicles['model_year'].min()), int(vehicles['model_year'].max())

#create a slider
year_range = st.slider('Choose years', value=(min_year, max_year), min_value=min_year, max_value=max_year)

actual_range = list(range(year_range[0], year_range[1]+1))

df_filtered = vehicles[(vehicles['manufacturer'] == selected_menu) & (vehicles['model_year'].isin(list(actual_range)))]

df_filtered


st.header('Price Analysis')
st.write(""" ###### Let's check how distribution of price varies depending on transmission, cylinders, body type, and condition""")

list_for_his = ['transmission', 'cylinders', 'type', 'condition']
selected_type = st.selectbox('Option for price distribution', list_for_his)

fig1 = px.histogram(vehicles, x='price', color=selected_type)
fig1.update_layout(title='<b> Split of price by {}<b>'.format(selected_type))

st.plotly_chart(fig1)

#add age column and age category
vehicles['age'] = 2024 - vehicles['model_year']

def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '5-10'
    elif x>=10 and x<=20: return '10-20'
    else: return '>20'
    
    
vehicles['age_category']  = vehicles['age'].apply(age_category)

list_for_scatter = ['odometer', 'cylinders', 'age']
choice_for_scatter = st.selectbox('Price dependency on', list_for_scatter)

fig2 = px.scatter(vehicles, x='price', y=choice_for_scatter, color="age_category")
fig2.update_layout(title='<b> Price vs {}<b>'.format(choice_for_scatter))
st.plotly_chart(fig2)
