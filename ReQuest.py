import streamlit as st

def month(num):
    if num=='1':  return 'January'
    if num=='2':  return 'February'
    if num=='3':  return 'March'
    if num=='4':  return 'April'
    if num=='5':  return 'May'
    if num=='6':  return 'June'
    if num=='7':  return 'July'
    if num=='8':  return 'August'
    if num=='9':  return 'September'
    if num=='10': return 'October'
    if num=='11': return 'November'
    if num=='12': return 'December

def number5(num):
    return '00000'[:5-len(str(num))]+str(num)

def number2(num):
    return '00'[:2-len(str(num))]+str(num)

def extract(pdf_name):
    with fitz.open(pdf_name) as doc:
        text = ''
        for page in doc:
            text = text+page.get_text()
        return text

def similarity(text1,text2):
    sequence = difflib.SequenceMatcher(None,text1,text2)
    return sequence.ratio()

def ani(frame):
    if frame>360: frame = 360
        with open('./publices.txt','r') as f:
            data = [i.split() for i in f]
        mem1,val1,col1 = str(data[1][0])+'\n'+str(data[1][1]),360.0*float(data[1][2])/sum([float(data[i][2]) for i in range(1,6)]),str(data[1][3])
        mem2,val2,col2 = str(data[2][0])+'\n'+str(data[2][1]),360.0*float(data[2][2])/sum([float(data[i][2]) for i in range(1,6)]),str(data[2][3])
        mem3,val3,col3 = str(data[3][0])+'\n'+str(data[3][1]),360.0*float(data[3][2])/sum([float(data[i][2]) for i in range(1,6)]),str(data[3][3])
        mem4,val4,col4 = str(data[4][0])+'\n'+str(data[4][1]),360.0*float(data[4][2])/sum([float(data[i][2]) for i in range(1,6)]),str(data[4][3])
        mem5,val5,col5 = str(data[5][0])+'\n'+str(data[5][1]),360.0*float(data[5][2])/sum([float(data[i][2]) for i in range(1,6)]),str(data[5][3])
        ax.clear()
        ax.set_aspect('equal')
        if float(frame)<=val1:
            val = [float(frame),360.0-float(frame)]
            cal = [col1,'white']
            mem = [mem1,]
        if float(frame)>val1 and float(frame)<=val1+val2:
            val = [val1,float(frame)-val1,360.0-float(frame)]
            cal = [col1,col2,'white']
            mem = [mem1,mem2]
        if float(frame)>val1+val2 and float(frame)<=val1+val2+val3:
            val = [val1,val2,float(frame)-val1-val2,360.0-float(frame)]
            cal = [col1,col2,col3,'white']
            mem = [mem1,mem2,mem3]
        if float(frame)>val1+val2+val3 and float(frame)<=val1+val2+val3+val4:
            val = [val1,val2,val3,float(frame)-val1-val2-val3,360.0-float(frame)]
            cal = [col1,col2,col3,col4,'white']
            mem = [mem1,mem2,mem3,mem4]
        if float(frame)>val1+val2+val3+val4 and float(frame)<=val1+val2+val3+val4+val5:
            val = [val1,val2,val3,val4,float(frame)-val1-val2-val3-val4,360.0-float(frame)]
            cal = [col1,col2,col3,col4,col5,'white']
            mem = [mem1,mem2,mem3,mem4,mem5]
        w,_ = ax.pie(val,colors=cal,startangle=0.0)
        ax.set_position([-0.18,0.0,1.0,1.0])
        centre_circle = plt.Circle((0, 0), 0.7, fc='white')
        ax.add_artist(centre_circle)
        Nrep = int(sum([float(data[i][2]) for i in range(1,6)])*frame/360)
        ax.text(0.0,0.0,f"{Nrep} reports",color='#007BFF',ha='center',va='center',fontsize=20,fontweight='bold')
        l = ax.legend(w,mem,title="",loc="center left",bbox_to_anchor=(0.9,0.0,0.5,1.0),frameon=False,fontsize=15)
        for text in l.get_texts():
            text.set_color('#007BFF')

def preprocess(text):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [word for word in words if word not in stop_words and word not in string.punctuation]
        processed_sentences.append(' '.join(words))
        return sentences,processed_sentences

def matches(question,sentences,processed_sentences,score):
    question_doc = nlp(question)
    scores = []
    for i,sent in enumerate(processed_sentences):
        sent_doc = nlp(sent)
        similarity = question_doc.similarity(sent_doc)
        if similarity>score: scores.append((sentences[i],similarity))
    scores = sorted(scores,key=lambda x: x[1],reverse=True)
    return scores

def synthesize(question,matches):
    answer = ' '.join([match[0] for match in matches])
    return answer
    
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
if submit:
    st.markdown('---')
    relevance = False
    text1 = extract(upload)
    rations = [0.0,]
    for exist in [f for f in Path('./Hub.dir').iterdir() if f.is_file()]:
        text2 = extract(exist)
        ratio = similarity(text1,text2)
        rations.append(ratio)
    if max(rations)<0.95:
        relevance = True
        time = datetime.datetime.now()
        doc = fitz.open(stream=upload.read(),filetype='pdf')
        st.write(':blue[Title:] %s'%(doc.metadata['title']))
        st.write(':blue[keywords:] %s'%(doc.metadata['keywords']))
        c1,c2 = st.columns([1,1])
        with c1:
            st.write(':blue[Author:] %s'%(doc.metadata['author']))
            st.write(':blue[Language:] %s'%(language(detect(text1))))
        with c2:
            st.write(':blue[Year:]',max([x for x in re.findall(r'\b[12]\d{3}\b',text1) if int(x)>=1950 and int(x)<=2030]))
            st.write(':blue[Pages:] %s'%(doc.page_count))
        st.markdown('---')
        c1,c2 = st.columns([1,1])
        if member=='--- None ---' or relevance==False:
            st.subheader(':warning: :red[Error in uploading...]')
            if member=='--- None ---': st.write(':x: :red[please select a valid member!]')
            if relevance==False: st.write(':x: :red[unfortunately the pdf already exists!]')
        else:
            comment = 'Upload: %s, %s %s:%s:%s %s %s'%(member,str(['0%s'%(x) if len(x)==1 else x for x in [str(time.day),]][0]),str(['0%s'%(x) if len(x)==1 else x for x in [str(time.hour),]][0]),str(['0%s'%(x) if len(x)==1 else x for x in [str(time.minute),]][0]),str(['0%s'%(x) if len(x)==1 else x for x in [str(time.second),]][0]),str(month(['0%s'%(x) if len(x)==1 else x for x in [str(time.month),]][0])),str(['0%s'%(x) if len(x)==1 else x for x in [str(time.year),]][0]))
            doc[0].insert_text((doc[0].rect.width-fitz.get_text_length(comment,fontsize=11)-10.0,10.0),comment,fontsize=11,color=(1,0,0))
            doc.save('./Hub.dir/p-%s.pdf'%(number5(len([f for f in Path('./Hub.dir').iterdir()])+1)))
            for i in range(0,len(Members)):
                if Members[i]==member: Publics[i] = Publics[i]+1
            with open('./publices.txt','w') as f:
                f.write('name     surname     publices     colors\n')
                for i in range(0,len(Members)):
                    f.write('%s   %d   %s\n'%(Members[i],Publics[i],Colors[i]))
                st.subheader(':ok_hand: :green[pdf was submitted successfully!]')
                fig,ax = plt.subplots()
                ax.set_aspect('equal')
                a = FuncAnimation(fig,ani,frames=np.arange(0,481,1),interval=100)
                a.save('./anim1.gif',writer=PillowWriter(fps=20))
