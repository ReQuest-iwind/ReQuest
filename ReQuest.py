import streamlit as st

with open('./publices.txt','r') as f:
    data = [i.split() for i in f]
Members = [str(data[i][0])+' '+str(data[i][1]) for i in range(1,len(data))]
Publics = [float(data[i][2]) for i in range(1,len(data))]
Colors  = [str(data[i][3]) for i in range(1,len(data))]

st.set_page_config(page_title='ReQuest',page_icon=":chart_with_upwards_trend:",layout="wide")

with st.container():
    col1,col2 = st.columns([7,1])
    with col1:
        st.header('**:blue[ReQuest]**',divider='blue')
    with col2:
        image = st.image('./logo.png',width=200)

col1,col2 = st.columns([1,1])

with col1:
    with st.form(key='upload'):
        st.subheader(':blue[PDF uploading]')
        member = st.selectbox(':blue[Who are you?]',options=['--- None ---',]+Members)
        upload = st.file_uploader(':blue[Upload your pdf file!]',type=['pdf'])
        submit = st.form_submit_button(':blue[Sumbit]',use_container_width=True)
