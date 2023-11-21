import streamlit as st
import pandas as pd
import os
import warnings
import plotly.express as px
import datetime as dt
warnings.filterwarnings('ignore')

# Link : https://www.youtube.com/watch?v=7yAw1nPareM

# Setup the Page configuration
st.set_page_config(page_title= '# SUPER STORE',
                   page_icon=':bar_chart:',
                   layout='wide')
st.write('# :bar_chart: Superstore EDA')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)   

# Upload the Datafile
fl = st.file_uploader(':file_folder: Upload a file' ,type=(['csv,xlsx,xls']))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding='ISO-8859-1')
else:
    os.chdir(r'C:\Users\shanm\OneDrive\Desktop\E2E\4_streamlitdashboard')
    df=pd.read_csv(r'superstore_csv.csv',encoding='ISO-8859-1')
#st.write(df.head(5))

# Date Picker
col1,col2 = st.columns(2)
df['Order Date'] = pd.to_datetime(df['Order Date'],format="%d-%m-%Y")
startDate=pd.to_datetime(df['Order Date']).min()
endDate=pd.to_datetime(df['Order Date']).max()

with col1:
    date1=pd.to_datetime(st.date_input('Start Date',startDate))
with col2:
    date2=pd.to_datetime(st.date_input('End Date',endDate))

# Filter the dataframe as per the date picker value
df=df[(df['Order Date']>=date1) & (df['Order Date']<=date2)].copy()
#st.write(df)

# Sidebar Creation for Region
st.sidebar.header('CHOOSE YOUR FILTER')
region = st.sidebar.multiselect('Pick your Region',df['Region'].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df['Region'].isin(region)]
#    st.write(df2)

# Sidebar Creation for State
state = st.sidebar.multiselect('Pick the States',df2['State'].unique()) # Provide only the states that are applicable as per the region selected
if not state:
    df3=df2.copy()
else:
    df3=df2[df2['State'].isin(state)]
    #st.write(df2)

# Sidebar Creation for City
city=st.sidebar.multiselect('Pick the City',df3['City'].unique())

# Filter the data base on Region,State and City
if not region and not state and not city:
    dfx = df

elif not state and not city: # ONLY REGION
    dfx=df[df['Region'].isin(region)]

elif not region and not city: # ONLY STATE
    dfx=df[df['State'].isin(state)]

elif state and city: # STATE AND CITY
    dfx=df3[df3['State'].isin(state) & df3['City'].isin(city)]

elif region and city: # REGION AND CITY
    dfx=df3[df3['Region'].isin(region) & df3['City'].isin(city)]

elif region and state: # REGION AND STATE
    dfx=df3[df3['Region'].isin(region) & df3['State'].isin(state)]

elif city: # ONLY CITY
    dfx=df3[df3['City'].isin(city)]

else: # ALL 3
    dfx=df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]

# Category Values
category = dfx.groupby(by=['Category'],as_index=False)['Sales'].sum()

# Chart Creation
with col1:
    st.subheader('Category Wise Sales')
    fig=px.bar(category,
               x='Category',
               y='Sales',
               text=['${:,.2f}'.format(x) for x in category['Sales']],
               template='seaborn')
    st.plotly_chart(fig,use_container_width=True,height=200)    

with col2:
    st.subheader('Region Wise Sales')
    fig=px.pie(dfx,
               values='Sales',
               names='Region',
               hole=0.5)
    fig.update_traces(text=dfx['Region'],
                      textposition='outside')
    st.plotly_chart(fig,use_container_width=True)

# Download the data based on selection
cl1,cl2=st.columns(2)
with cl1:
    with st.expander('Category Viewdata'):
        st.write(category.style.background_gradient(cmap='Blues'))
        csv=category.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data',data=csv,file_name='Category.csv',mime='text/csv',help='click here to download data as a csv file')
            
with cl2:
    with st.expander('Region Viewdata'):
        region=dfx.groupby(by='Region',as_index=False)['Sales'].sum()
        st.write(category.style.background_gradient(cmap='Oranges'))
        csv=region.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data',data=csv,file_name='Region.csv',mime='text/csv',help='click here to download data as a csv file')


               











