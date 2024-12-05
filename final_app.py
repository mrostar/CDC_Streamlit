import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt

# page configuration
st.set_page_config(layout = "wide", initial_sidebar_state='expanded')

# initializes the current page in the session state if non-existing
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Introduction'

# intializes the filter selection(s) in the session state
if "age_ranges" not in st.session_state:
    st.session_state.age_ranges = ["85 years and over"]

# caching data for faster processing time
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df
df = load_data('streamlit_data.csv')

# defines what to do when you click on a button
def switch_page(page: str):
    st.session_state.current_page = page

# creating buttons/navigation 
st.sidebar.subheader('Navigation')

intro_button = st.sidebar.button(
    'Introduction'.upper(), on_click=switch_page, args=['Introduction']
)
age_range_button = st.sidebar.button(
    'Age Range Analysis'.upper(), on_click=switch_page, args=['Age Range Analysis']
)

# introduction page
def intro_page():
    st.title('CDC Suicide Analysis Project')
    st.write('Suicide is one of the leading causes of death in the United States, affecting people of all ages and races. In just 2018 alone, there were 48,344 deaths by suicide. This was the 10th leading cause of death that year. The data is taken from the CDC, and the dashboards are designed to visualize trends in suicide death rates in the United States.')

# avg estimate by age range page
def age_page():
    st.title('CDC Suicide Analysis Project')

    # Creating filters for features (age and year)
    st.sidebar.header('Selecting an age range to update the graph')

    unique_ages = sorted(df['AGE'].unique())
    unique_ages = [age for age in unique_ages if age != 'All ages']

    age_ranges = st.sidebar.multiselect(
        "Select Age Range(s)", unique_ages, 
        default = st.session_state.age_ranges)
    
    st.session_state.age_ranges = age_ranges
    
    # creating the line graph based on the filters
    filtered_data = df[df['AGE'].isin(st.session_state.age_ranges)]
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


fn_map = {
    'Introduction': intro_page,
    'Age Range Analysis': age_page
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, intro_page)
main_workflow()