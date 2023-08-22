'''
utils.py consists of all template, input and other utility functions of AnswerBot
'''

import streamlit as st ###### Import Streamlit library
from streamlit_chat import message ###### Import message function from streamlit_chat library to render chat
from configparser import ConfigParser ###### Import ConfigParser library to read config file for greeting
from chat import initialize_chat ###### Import initialize_chat function from chat.py to initialise chat upon clearing session state
from PIL import Image ###### Import Image from PIL library to save image uploaded by user
import os

####
config_object = ConfigParser() ###### Read config file for greeting
config_object.read("./config.ini") #
greeting=config_object["MSG"]["greeting"] #
###

def api_selector():
    input_choice = st.sidebar.radio("#### :blue[Choose the LLM]", ("OpenAI's GPT-3 [text-davinci-003]", "Meta-Llama-2 [llama-2-7b-chat]"))
    return input_choice
        

#### function to display document input options and return the input choice and uploaded file
#### this function is called from the main.py file
def input_selector():
        input_choice=st.sidebar.radio("#### :blue[Choose the Input Method]",('Document','Weblink','YouTube','Audio','Image', 'File Directory'))
        if input_choice=="Document":
            with st.sidebar.expander("📁 __Documents__",expanded=True):
                uploaded=st.file_uploader(label="Select File",type=['pdf','txt'],on_change=clear)
        elif input_choice=="Weblink":
            with st.sidebar.expander("🌐 __Webpage__",expanded=True):
                uploaded=st.text_input('Enter a weblink',on_change=clear)
        elif input_choice=="YouTube":
            with st.sidebar.expander("🎥 __YouTube__",expanded=True):
                uploaded=st.text_input('Enter a YT link',on_change=clear)
        elif input_choice=="Audio":
            with st.sidebar.expander("🎙 __Audio__",expanded=True):
                uploaded=st.file_uploader('Select File',type=['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav'],on_change=clear)
        elif input_choice=="Image":
            with st.sidebar.expander("🎙 __Text from Image__",expanded=True):
                uploaded=st.file_uploader('Select File',type=['jpg','jpeg','png'],on_change=clear, disabled=True)
                if uploaded:
                    image=Image.open(uploaded)
                    loc='./Assets/'+str(uploaded.name)
                    image.save(loc)
        elif input_choice=="File Directory":
            with st.sidebar.expander("__File Directory__", expanded=True):
                uploaded=st.file_uploader(label="Select File",type=['pdf','txt', 'docx'],on_change=clear, accept_multiple_files=True)

        return input_choice, uploaded


#### display function for the first column of the app homepage and info page
#### this function is called from the main.py file
def first_column():
            st.markdown("<p style='text-align:center; color:black;'><u><b>About Me</b></u></p>",unsafe_allow_html=True)
            st.markdown("<p style='color:#5A5A5A;'>🖖 I am a QnA agent that answers questions by reading assets (like documents, spreadsheets, videos, audios) provided by you.</p>",unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.write(" ")            
            st.markdown("<span style='color:#5A5A5A;'>🖖 I am built on [Streamlit](https://streamlit.io/) using large language models and a diverse set of document loaders developed by [LangChain](https://python.langchain.com/en/latest/index.html). A huge shout-out to [Stremlit Chat](https://github.com/AI-Yash/st-chat) and [pdfplumber](https://github.com/jsvine/pdfplumber).</span>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.markdown("<p style='color:#5A5A5A;'>🖖 Presently, Documents(.pdf and .txt), web ulrs(single page), YouTube links, Audio files and text from Images are enabled. Websites and Spreadsheets are next in pipeline.</p>", unsafe_allow_html=True)
            st.write(" ")        
            st.write(" ")        


#### display function for the second column of the app homepage and info page
#### this function is called from the main.py file
def second_column():
            st.markdown("<p style='text-align:center; color:black;'><u><b>How to Use</u></b></p>",unsafe_allow_html=True)
            st.markdown("<span style='color:#5A5A5A;'>👉🏽 Firstly, you need to enter your api key🔧 in the input box on the sidebar.</span>",unsafe_allow_html=True)
            with st.expander("About the API"):
                st.markdown("<span style='color:#5A5A5A;'>🌟 AnswerBot uses Llama-2-7b-chat hosted on aws using FastAPI. You'll require a key to access the api. Currently, we uses a smaller model which could limits the quality of output generated.",unsafe_allow_html=True)

            st.markdown("<span style='color:#5A5A5A;'>👉🏽 You can then choose the asset you want to chat on. From the radio buttons on the sidebar. Presently you can select 📜 documents or 🔗 links to webpages, YouTube videos, images basis your choice.",unsafe_allow_html=True)
            st.write(" ")
            st.markdown("<span style='color:#5A5A5A;'>👉🏽 AnswerBot is ready ✌. You can ask your question. Also, explore summary tab to generate document summary, extract talking points and look at sample questions.",unsafe_allow_html=True)
            st.markdown("<span style='color:#5A5A5A;'>👉🏽 Also note, the app wouldn't work without an active internet connection🌐",unsafe_allow_html=True)

#### display function for the third column of the app homepage and info page
#### this function is called from the main.py file
def third_column():
            st.markdown("<p style='text-align:center;color:black;'><u><b>Roadmap & Suggestions</b></u></p>",unsafe_allow_html=True)
            st.markdown("<p style='color:#5A5A5A;'>🎯 Spreadsheets and Codes as inputs. Ability to handle multiple inputs, complete websites, content repositories etc.</p>",unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.markdown("<p style='color:#5A5A5A;'>🎯 Analysis of spreadsheets with charts📊 and insights✍. Analysis of other forms of dataframes/datasets.",unsafe_allow_html=True)
            st.markdown("<p style='color:#5A5A5A;'>🎯 Use models and embeddings that are free of cost.",unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.markdown("<span style='color:#5A5A5A;'>🎯 Please share your suggestions, issues, features requests, etc.",unsafe_allow_html=True)

#### display function for the header display
def heads():
    st.markdown("<h3 style='text-align:center;'>👋🏽 Welcome! I am <span style='color:#d81e19'>AnswerBot</span>!👩🏽‍💻</h3>",unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align:center;'>I answer questions after reading documents, webpages, images with text, YouTube videos, audio files.</p>
    """,unsafe_allow_html=True)
    st.markdown("<h6 style='text-align:center;'> Ask & Learn :)</h6>",unsafe_allow_html=True)

#### display function for the contact info
def contact():
    st.markdown("Email : [makshay@sigmoidanalytics.com](mailto:makshay@sigmoidanalytics.com)")

#### function to clear the cache and initialize the chat
def clear(greeting=greeting):
    with st.spinner("Clearing all history..."):
        st.cache_data.clear()
        if 'history' in st.session_state:
            del st.session_state['history']
        if 'pastinp' in st.session_state:
            del st.session_state['pastinp']
        if 'pastresp' in st.session_state:
            del st.session_state['pastresp']

        initialize_chat(greeting)

### This function for writing chat history into a string variable called hst
### This function is called from the main.py file
### This function is called when the user clicks on the download button
def write_history_to_a_file():
    hst=""
    st.session_state['history']=[]
    st.session_state['history'].append("AnswerBot says -")
    st.session_state['history'].append(st.session_state['pastresp'][0])
    for i in range(1,len(st.session_state['pastresp'])):
        st.session_state['history'].append("Your Query - ")
        st.session_state['history'].append(st.session_state['pastinp'][i-1])
        st.session_state['history'].append("AnswerBot's response - ")
        st.session_state['history'].append(st.session_state['pastresp'][i])

    for item in st.session_state['history']:
        hst+="\n"+str(item)
    
    return hst
