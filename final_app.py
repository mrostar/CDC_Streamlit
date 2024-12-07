import streamlit as st
import pandas as pd
import altair as alt

# page configuration
st.set_page_config(layout = "wide", initial_sidebar_state='expanded')

# caching data for faster processing time
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df
df = load_data('streamlit_data.csv')

# initializes the current page in the session state if non-existing
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Introduction'

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

    st.sidebar.header('Filter Graph by Year')

    default_years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2018]

    selected_years = st.sidebar.multiselect(
        "Select Year(s):", 
        options=sorted(df['YEAR'].unique()), 
        default= default_years
    )

    filtered_data = df[df['YEAR'].isin(selected_years)]

    avg_estimates_by_year = filtered_data.groupby('YEAR')['ESTIMATE'].mean().round(2).reset_index()

    bar_chart = alt.Chart(avg_estimates_by_year).mark_bar(color='orange').encode(
            x=alt.X('YEAR:O', title='Year'),  
            y=alt.Y('ESTIMATE:Q', title='Average Estimate'),   
            tooltip=[
                alt.Tooltip('YEAR:O', title='Year'),
                alt.Tooltip('ESTIMATE:Q', title='Average Estimate'),
            ]  
        ).properties(
            title='Average Estimate Over Time'
        )


    line_chart = alt.Chart(avg_estimates_by_year).mark_line(color='blue').encode(
        x=alt.X('YEAR:O'),  
        y=alt.Y('ESTIMATE:Q'),
        tooltip=[
            alt.Tooltip('YEAR:O', title='Year'),
            alt.Tooltip('ESTIMATE:Q', title='Average Estimate')
        ]
    )
    layered_chart = (bar_chart + line_chart).properties(
            title='Average Estimates Over Time'
        )
        
    st.altair_chart(layered_chart, use_container_width=True)



############################
# avg estimate by age range page
def age_page():
    st.title('Average Estimates By Age Range from 1950 to 2018')

    # Creating filters for features (age and year)
    st.sidebar.header('Filter Graph by Year')

    unique_ages = sorted(df['AGE'].unique())
    unique_ages = [age for age in unique_ages if age != 'All ages']
    
    # age_selection = [] 
    age_ranges = st.sidebar.multiselect(
        "Select Age Range(s)", unique_ages,  
        default = ['85 years and over'])
    
    st.session_state.age_ranges = age_ranges
    
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


fn_map = {
    'Introduction': intro_page,
    'Age Range Analysis': age_page
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, intro_page)
main_workflow()