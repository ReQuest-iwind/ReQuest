import streamlit as st

st.set_page_config(page_title='ReQuest',page_icon=":chart_with_upwards_trend:",layout="wide")

with st.container():
    col1,col2 = st.columns([7,1])
        with col1:
          st.header('**:blue[ReQuest]**',divider='blue')
        with col2:
          image = st.image('./logo.png',width=200)
