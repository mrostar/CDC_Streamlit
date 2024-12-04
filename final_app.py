import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt

st.set_page_config(layout='wide')

df = pd.read_csv('streamlit_data.csv')

st.title('CDC Suicide Analysis Project')


# Creating filters for features (age and year)
st.sidebar.header('Select Features')

unique_ages = sorted(df['AGE'].unique())
unique_ages = [age for age in unique_ages if age != 'All ages']
age_ranges = st.sidebar.multiselect("Select Age Range(s)", unique_ages)


# creating the line graph based on the filters
filtered_data = df[df['AGE'].isin(age_ranges)]
avg_estimates_year_age = filtered_data.groupby(['YEAR', 'AGE'])['ESTIMATE'].mean().reset_index()

line_chart = alt.Chart(avg_estimates_year_age).mark_line().encode(
    x=alt.X('YEAR:O', title='Year'),  
    y=alt.Y('ESTIMATE:Q', title='Average Estimate'),  
    color='AGE:N',  
    tooltip=[
        alt.Tooltip('YEAR:O', title='Year'),
        alt.Tooltip('AGE:N', title='Age Range'),
        alt.Tooltip('ESTIMATE:Q', title='Average Estimate')
    ]  
).properties(
    title='Average Estimate by Age Range Over Time'
)
st.altair_chart(line_chart, use_container_width=True)

#add buttons
