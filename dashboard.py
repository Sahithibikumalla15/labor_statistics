import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data_setup import *

instance = LaborData(owner='developer')

def yearmonth(df):

    # Mapping of month names to month numbers
    month_map = {
        'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
        'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
    }

    # Create yearMonth column by combining 'year' and 'month' (mapped to month number)
    df['yearMonth'] = df['year'].astype(str) + '-' + df['periodName'].map(month_map)

    return df





# Configure the page layout to 'wide'
st.set_page_config(page_title="Labor Statistics Dashboard", layout="wide")

# Set the title of the dashboard
st.title("Labor Statistics Real Time Dashboard")

# Create two columns
col1, col2 = st.columns(2)


civilian_employment =  pd.read_csv('data/LNS12000000.csv')

civilian_unemployment =  pd.read_csv('data/LNS13000000.csv')

civilian_employment.loc[:,'category']='employed'
civilian_unemployment.loc[:,'category']='unemployed'


emp_vs_unemp =pd.concat([civilian_employment,civilian_unemployment],ignore_index=True)

emp_vs_unemp.drop(columns='footnotes',inplace=True)

emp_vs_unemp = yearmonth(emp_vs_unemp)


# Line chart in the first column
with col1:
    # st.subheader("Unemployment Vs Employment Trend")
    fig = px.line(
        emp_vs_unemp,
        x="yearMonth",
        y="value",
        color="category",  # Split lines by 'Category'
        # barmode='group',
        title="Monthly Trends Employment Vs Unemployment",
    )
    st.plotly_chart(fig, use_container_width=True)

# Data in the second column
with col2:
    # st.subheader("Latest Numbers")

    emp_vs_unemp.sort_values(by='yearMonth',ascending=False,inplace=True)

    fig = px.pie(emp_vs_unemp.loc[:2], names='category', 
    values='value', title='Employed Vs Unemployed (Latest)')

    # Display the chart in Streamlit
    st.plotly_chart(fig)


# Create two columns
col3, col4 = st.columns(2)

emp_vs_unemp.sort_values(by='yearMonth',ascending=False,inplace=True)

# Data in the second column
with col3:

    st.write('Raw Data For Unemployed')

    st.dataframe(emp_vs_unemp.loc[emp_vs_unemp['category']=='unemployed'])

# Data in the second column
with col4:

    st.write('Raw Data For Employed')

    st.dataframe(emp_vs_unemp.loc[emp_vs_unemp['category']=='employed'])

# Section 2: Man hours worked

# Create two columns
col5, col6 = st.columns(2)

all_employee_hrs =  pd.read_csv('data/CES0500000002.csv')

prod_enmployees =  pd.read_csv('data/CES0500000007.csv')

all_employee_hrs.loc[:,'category']='all_employees'

prod_enmployees.loc[:,'category']='prod_employees'

hours_worked_df =pd.concat([all_employee_hrs,prod_enmployees],ignore_index=True)

hours_worked_df.drop(columns='footnotes',inplace=True)

hours_worked_df = yearmonth(hours_worked_df)


# Line chart in the first column
with col5:
    # st.subheader("Unemployment Vs Employment Trend")
    fig = px.bar(
        hours_worked_df,
        x="year",
        y="value",
        color="category",  # Split lines by 'Category'
        barmode='group',
        title="Employee Work Hours All Employee Vs Production Employees",
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:

    st.subheader('Raw Data For Work Hours')

    st.dataframe(hours_worked_df.sort_values(by='yearMonth',ascending=False)[['year','periodName','category','value']])

# section 3 earning of employees

all_employee_hrs_earnings =  pd.read_csv('data/CES0500000003.csv')

prod_enmployees_earnings =  pd.read_csv('data/CES0500000008.csv')

all_employee_hrs_earnings.loc[:,'category']='all_employees'

prod_enmployees_earnings.loc[:,'category']='prod_employees'

earnings_df =pd.concat([all_employee_hrs_earnings,prod_enmployees_earnings],ignore_index=True)

earnings_df.drop(columns='footnotes',inplace=True)

earnings_df = yearmonth(earnings_df)



# Create two columns
col7, col8 = st.columns(2)


with col7:
    # st.subheader("Unemployment Vs Employment Trend")
    fig = px.bar(
        earnings_df,
        x="year",
        y="value",
        color="category",  # Split lines by 'Category'
        barmode='group',
        title="Employee Hourly Earnings All Employee Vs Production Employees",
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:

    st.subheader('Raw Data For Hourly Earning')

    st.dataframe(earnings_df.sort_values(by='yearMonth',ascending=False)[['year','periodName','category','value']])


# Add a button to trigger the reload
if st.button('Refresh Data',):    

    instance.fulfill_incremantal_load()

    # This will cause the app to rerun
    st.rerun()



    
    




