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

# if "age_ranges" not in st.session_state:
#     st.session_state.age_ranges = 'Age Range Analysis'

# defines what to do when you click on a button
def switch_page(page: str):
    st.session_state.current_page = page

# creating buttons/navigation 
st.sidebar.subheader('Navigation')

intro_button = st.sidebar.button(
    'Introduction'.upper(), on_click=switch_page, args=['Introduction'])

age_range_button = st.sidebar.button(
    'Age Range Analysis'.upper(), on_click=switch_page, args=['Age Range Analysis'])

gender_button =  st.sidebar.button(
    'Gender Analysis'.upper(), on_click=switch_page, args=['Gender Analysis']) 

gender_button =  st.sidebar.button(
    'Race/Ethnic Group Analysis'.upper(), on_click=switch_page, args=['Race/Ethnic Group Analysis']) 


#################
# introduction page
def intro_page():
    st.markdown("<h1 style='text-align: center;'>CDC Suicide Analysis Project</h1>", unsafe_allow_html=True)
    st.write('Suicide is one of the leading causes of death in the United States, affecting people of all ages and races. In just **2018** alone, there were **48,344** deaths by suicide. This was the **10th** leading cause of death that year. The data is taken from the CDC, and this streamlit app is designed to visualize trends in suicide death rates in the United States.')

    st.sidebar.header('Filter Graph by Year')

    default_years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2018]

    selected_years = st.sidebar.multiselect(
        "Select Year(s):", 
        options=sorted(df['YEAR'].unique()), 
        default= default_years)

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
# try to tilt the x axis (years)

    line_chart = alt.Chart(avg_estimates_by_year).mark_line(color='blue').encode(
        x=alt.X('YEAR:O'),  
        y=alt.Y('ESTIMATE:Q'),
        tooltip=[
            alt.Tooltip('YEAR:O', title='Year'),
            alt.Tooltip('ESTIMATE:Q', title='Average Estimate')])

    layered_chart = (bar_chart + line_chart).properties(
            title='Average Estimates Over Time'
        ).configure_title(anchor = 'middle')
        
    st.altair_chart(layered_chart, use_container_width=True)

   
    st.markdown(
         """
        <div style='font-size: 15px; line-height: 1.6; text-align: center; width: 100%; padding: 20px;'>
         <strong>Definition of estimate</strong>: The calculated estimate of the measure. 
         In this case, the measure is the death rate for suicide in the United States, measured 
          as deaths per 100,000 residents (crude estimate).
          </div>
          """, 
          unsafe_allow_html=True)

    df_filtered = df.dropna(subset=['ESTIMATE'])
    df_filtered['YEAR']= df_filtered['YEAR'].astype(str)

    avg_estimates_by_year = df_filtered.groupby('YEAR').agg( 
    avg_estimate=('ESTIMATE', 'mean'), num_observations=('ESTIMATE', 'size')).reset_index()
    
    avg_estimates_by_year['avg_estimate'] = avg_estimates_by_year['avg_estimate'].round(2)
    avg_estimates_by_year = avg_estimates_by_year.sort_values(by='avg_estimate', ascending=False)

    avg_estimates_by_year = avg_estimates_by_year.rename(columns={
        'YEAR': 'Year',
        'avg_estimate': 'Avg Estimate',
        'num_observations': '# of non-null estimate taken'})

    st.dataframe(avg_estimates_by_year, use_container_width=True)

    
#################
# avg estimate by age range page
def age_page():
    st.title('Average Estimates By Age Range from 1950 to 2018')

    # Creating filters for features (age and year)
    st.sidebar.header('Filter Graph by Age Range')

    unique_ages = sorted(df['AGE'].unique())
    unique_ages = [age for age in unique_ages if age != 'All ages']
    
    default_ages = ['85 years and over', '55-64 years', '35-44 years', '10-14 years'] 
    age_ranges = st.sidebar.multiselect(
        "Select Age Range(s)", unique_ages,  
        default = default_ages)
    
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
    ).properties(title='Average Estimate by Age Range Over Time'
                 ).configure_title(anchor = 'middle')

    st.altair_chart(line_chart, use_container_width=True)

    st.write("""
        Older people tend to have higher estimates than younger people, 
        with the highest average coming in the year **1991**, where people 
        ages **85 years and above** had an average estimate of **43.58**. As you age, your health **decreases**, 
        you become more susceptible to **loneliness**, and you often become **dependent** on others. 
        All of these things can lead to **higher** rates of suicide.
    """)



#################
def gender_page():
    st.markdown("<h1 style='text-align: center;'>What gender is at most risk?</h1>", unsafe_allow_html=True)

    st.write("""
        **Males** tend to have a much higher suicide rate than **females**, 
        with their average estimate being approximately **3.8x** higher (across all years).
    """)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.sidebar.header('Filter Graph by Year')
    default_years = [2014, 2015, 2016, 2017, 2018]

    selected_years = st.sidebar.multiselect(
        "Select Year(s):", 
        options=sorted(df['YEAR'].unique()), 
        default= default_years)

    filtered_data = df[df['YEAR'].isin(selected_years)]

    male_data = filtered_data[filtered_data['STUB_LABEL'] == 'Male']
    avg_estimates_male = male_data.groupby('YEAR')['ESTIMATE'].mean().reset_index()
    overall_avg_male = avg_estimates_male['ESTIMATE'].mean()

    female_data = filtered_data[filtered_data['STUB_LABEL'] == 'Female']
    avg_estimates_female = female_data.groupby('YEAR')['ESTIMATE'].mean().reset_index()
    overall_avg_female = avg_estimates_female['ESTIMATE'].mean()


    male_chart = (
    (
        alt.Chart(avg_estimates_male)
        .mark_bar(color='#7BAFD4')
        .encode(
            x=alt.X('YEAR:O', title='Year'),  
            y=alt.Y('ESTIMATE:Q', title='Average Estimate'),  
            tooltip=[
                alt.Tooltip('YEAR:O', title='Year'),
                alt.Tooltip('ESTIMATE:Q', title='Average Estimate')
            ]  
        )
        + alt.Chart(pd.DataFrame({'y': [round(overall_avg_male, 2)]}))
        .mark_rule(color='black', strokeDash=[4, 2])
        .encode(
            y='y:Q',
            tooltip=[alt.Tooltip('y:Q', title='Overall Average')])
    )
    .properties(title='Average Estimate for Males Over Time'
    )
    .configure_title(anchor='middle', fontSize=13))


    female_chart = (
    (
        alt.Chart(avg_estimates_female)
        .mark_bar(color='pink')
        .encode(
            x=alt.X('YEAR:O', title='Year'),
            y=alt.Y('ESTIMATE:Q', title='Average Estimate'),
            tooltip=[
                alt.Tooltip('YEAR:O', title='Year'),
                alt.Tooltip('ESTIMATE:Q', title='Average Estimate')
            ]
        )
        + alt.Chart(pd.DataFrame({'y': [round(overall_avg_female, 2)]}))
        .mark_rule(color='black', strokeDash=[4, 2])
        .encode(
            y='y:Q',
            tooltip=[alt.Tooltip('y:Q', title='Overall Average', format=".2f")])
    )
    .properties(title='Average Estimate for Females Over Time'
    )
    .configure_title(anchor='middle', fontSize=13))


    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(male_chart, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; font-size: 16px;">
            Average <strong>male</strong> estimate (all years): <strong>19.34</strong>
        </div>
        """, unsafe_allow_html=True)
    

    with col2: 
        st.altair_chart(female_chart, use_container_width=True)
        st.markdown("""
        <div style="text-align: center; font-size: 16px;">
            Average <strong>female</strong> estimate (all years): <strong>5.05</strong>
        </div>
        """, unsafe_allow_html=True)


#################
def ethnic_page():
    st.markdown("<h1 style='text-align: center;'>What race/ethnic group is at most risk?</h1>", unsafe_allow_html=True)
    st.write("""
             Across all years, **non-Hispanic or Latino American Indian or Alaskan Native 
             males** had the highest rate, with an average of **25.67**. In comparison, across all years, 
             **Hispanic or Latino (all races) females** had the lowest rate, with an average of **1.93**.
             """)
    
    st.sidebar.header('Filter Graph By Year')

    default_years = [2014, 2015, 2016, 2017, 2018]

    selected_years = st.sidebar.multiselect(
            "Select Year(s):", 
            options=sorted(df['YEAR'].unique()), 
            default=default_years)

    filtered_data = df[df['YEAR'].isin(selected_years)]


    ethnic_groups = [
        "Male: Not Hispanic or Latino: American Indian or Alaska Native", 
        "Male: Not Hispanic or Latino: Black or African American", 
        "Male: Hispanic or Latino: All races", 
        "Male: Not Hispanic or Latino: Asian or Pacific Islander", 
        "Male: Not Hispanic or Latino: White", 
        "Female: Not Hispanic or Latino: American Indian or Alaska Native", 
        "Female: Not Hispanic or Latino: Black or African American", 
        "Female: Hispanic or Latino: All races", 
        "Female: Not Hispanic or Latino: Asian or Pacific Islander", 
        "Female: Not Hispanic or Latino: White"
        ]


    filtered_data = filtered_data[filtered_data['STUB_LABEL'].isin(ethnic_groups)]
    filtered_data = filtered_data[filtered_data['STUB_NAME'] == 'Sex and race and Hispanic origin']

    avg_estimates_race = filtered_data.groupby('STUB_LABEL')['ESTIMATE'].mean().reset_index()

    chart = alt.Chart(avg_estimates_race).mark_bar().encode(
        x=alt.X('STUB_LABEL:N', title='Race/Ethnicity', sort='-y'),  
        y=alt.Y('ESTIMATE:Q', title='Average Estimate'),  
        color='STUB_LABEL:N',  
        tooltip=['STUB_LABEL:N', 'ESTIMATE:Q']  
    ).properties(
        title='Average Suicide Estimate by Race/Ethnicity Across Selected Years'
    ).configure_axis(
        labelAngle=-45).configure_title(anchor='middle')
    

    st.altair_chart(chart, use_container_width=True)


#################
fn_map = {
    'Introduction': intro_page,
    'Age Range Analysis': age_page,
    'Gender Analysis': gender_page,
    'Race/Ethnic Group Analysis': ethnic_page
}
main_window = st.container()
main_workflow = fn_map.get(st.session_state.current_page, intro_page)
main_workflow()
