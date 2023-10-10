import streamlit as st
import time
import pandas as pd
from pytube import YouTube
import re

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    sanitized_filename = re.sub(r'[\/:*?"<>|]', '_', filename)
    return sanitized_filename


url = "https://www.youtube.com/watch?v=aywZrzNaKjs"
yt = YouTube(url)

outfile_path = f"YoutubeVideoTranscribeQAData/{sanitize_filename(yt.title)}"
data = pd.read_csv(f'{outfile_path}/question_answer.csv')
count = len(data)
def toggle_widget(i):
    text = st.session_state[f"t{i}"]
    if st.session_state.widget_disabled[i]==False:
        st.session_state.widget_disabled[i] = True
       
        
    return text
     

if 'widget_disabled' not in st.session_state:
    st.session_state.widget_disabled = [False]*count
    
    
st.title("YouTube QA Bot")

st.markdown(f"**Youtube video link :**[Langchain in 13 minutes]({url})")
    # Get YouTube video URL from user
st.write("Hey! Have you watched above youtube link video...")

checkbox_state = st.checkbox("If yes please check this box...\n, otherwise please watch the above youtube video and come back...")

flag = 0

if checkbox_state:
    scores = []
    
    st.subheader("Plase type your answers for below following questions")
    
    for i in range(0,count):
        st.write(data['Question'][i])
        wid = st.text_input(placeholder='enter your answer here',label='ans',
                        label_visibility='collapsed',
                        key=f"t{i}",
                        on_change=toggle_widget,args=(i,) ,
                        disabled=st.session_state.widget_disabled[i])
        if wid:
            
            st.text(f"your answer: {wid}")
            for ans in data['Answer'][i]:
                val_count = 0
                for ans2 in wid.split(' '):
                    if ans2 in data['Answer'][i].lower().split(' '):
                        val_count = val_count+1
            score = val_count / len(data['Answer'][i].lower().split(' '))
            scores.append(score)
            st.markdown(f"**your score is** : {score}/1")
            flag = flag+1
            
            if flag==count:
                final_score = sum(scores)/count
                if final_score>0.5:
                    st.markdown(f"**Your final score: {final_score}**")
                    st.markdown("\n\n")
                    st.markdown("===============================================================")
                    st.markdown("\n\n")
                    st.markdown(f"**Thank you for watching the video**")
                    st.markdown("\n\n")
                    st.markdown("===============================================================")
                else:
                    st.markdown(f"**Your final score: {final_score}**")
                    st.markdown("\n\n")
                    st.markdown("===============================================================")
                    st.markdown("\n\n")
                    st.markdown("**Please watch the above youtube video and come back...**")
                    st.markdown("\n\n")
                    st.markdown("===============================================================")
        else:
            break
    
        
        
else:
    pass


