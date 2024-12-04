import streamlit as st
import pandas as pd
import seaborn as sns

st.title('CDC Suicide Analysis Project')

df = pd.read_csv('streamlit_data.csv')

st.markdown('example')