#### Main pythonfile to run the app on streamlit ####
#### There are five more python files in the src folder ####
#### Each python file has a specific function and is imported in this file ####
#### The python files are: ####
#### 1. loaders.py - contains functions to load input from different sources ####
#### 2. textgeneration.py - contains functions to generate text from input ####
#### 3. utils.py - contains utility functions ####
#### 4. api.py - contains functions to check and validate the OpenAI API key ####
#### 5. chat.py - contains functions to initialize and run the chatbot ####
#### apart from these, config.ini - contains the configuration for the app ####
#### and requirements.txt - contains the list of libraries required to run the app ####
#### The app can be run locally by running the command 'streamlit run src/main.py' ####


###### Import libraries ######
import streamlit as st ###### Import Streamlit library
from configparser import ConfigParser ###### Import ConfigParser library for reading config file to get model, greeting message, etc.
from PIL import Image ###### Import Image library for loading images
import openai ###### Import OpenAI library
import os ###### Import os library for environment variables
from utils import * ###### Import utility functions
from loaders import create_embeddings, faiss_db_file_name, check_upload ###### Import functions to load input from different sources
from textgeneration import llm_response, search_context, summary, talking, questions ###### Import functions to generate text from input
from api import check_key, validate_key, input_key ###### Import functions to check and validate the OpenAI API key
from chat import initialize_chat, render_chat, chatbot 
 

#### Create config object and read the config file ####
config_object = ConfigParser()
config_object.read("config.ini")

#### Initialize variables and reading configuration ####
logo = Image.open(config_object["IMAGES"]["logo_address"]) #### Logo for the sidebar
favicon = Image.open(config_object["IMAGES"]["favicon_address"]) #### Favicon

openai_models = config_object["MODEL"]["openai_model"] ##### model for GPT call
greeting=config_object["MSG"]["greeting"] ###### initial chat message

#### Set Page Config ####
st.set_page_config(layout="wide", page_icon=favicon, page_title="Sigmoid-AnswerBot") ###### Set page layout, favicon and title

#### Set Logo on top sidebar ####
# st.sidebar.image(hline) ###### Add horizontal line
c1, c2, c3 = st.sidebar.columns([1,3,1]) 

c2.markdown("""<hr style="width:170%;height:2px;border:none;color:red;background-color:red;margin-left:-35%;text-align:center" /> """, unsafe_allow_html=True)
c2.image(logo) ###### Add logo to middle column
c2.markdown("""<hr style="width:170%;height:2px;border:none;color:red;background-color:red;margin-left:-35%;text-align:center" /> """, unsafe_allow_html=True)

model_api = api_selector()
# Set the initial value of variables
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None
if "validation" not in st.session_state:
    st.session_state["validation"] = None
if "uploaded" not in st.session_state:
    st.session_state["uploaded"] = False
if "string_data" not in st.session_state:
    st.session_state["string_data"] = None
if "token" not in st.session_state:
    st.session_state["token"] = None
if "succeed" not in st.session_state:
    st.session_state["succeed"] = None
if "page" not in st.session_state:
    st.session_state["page"] = None
if "words" not in st.session_state:
    st.session_state["page"] = None

# Step 1 - Check if OpenAI Key is present, otherwise open the key input form -------------------------------------------
if (st.session_state["api_key"] is None) or (st.session_state["uploaded"]==False): 
    print("Entered Step 1")
    if check_key():
        # Check if API Key is valid, else show the 'Chante API Key' button
        if validate_key(model_api):
            input_choice, uploaded = input_selector() ###### Get input choice and input document
            print(input_choice, type(uploaded), uploaded)
            if (uploaded is not None) and (uploaded != ""):
                with st.spinner("reading "+input_choice+"..." if input_choice!="YouTube" else "extracting audio from YouTube..." if input_choice=="YouTube" else "extracting text from image..."): ###### Wait while input is being read
                    words, pages, string_data, succeed, token = check_upload(uploaded=uploaded, input_choice=input_choice) 
                    st.session_state["uploaded"] = True
                    st.session_state["words"] = words
                    st.session_state["pages"] = pages
                    st.session_state["string_data"] = string_data
                    st.session_state["succeed"] = succeed
                    st.session_state["token"] = token
        else:
            if st.sidebar.button("Change API Key", key="Uno"): ###### If key is not valid, show 'Change API' button
                input_key()

# ----------------------------------------------------------------------------------------------------------------------

# print("Before entering step 2", st.session_state["api_key"])

#### If input mode has been chosen and link/doc provided, convert the input to text ####
if (st.session_state["api_key"] is not None) and (st.session_state["uploaded"]==True):
        ###### Get input text from input document
        ###### words - number of words in the input
        ###### pages - number of embeddings in the input
        ###### string_data - input text
        ###### succeed - boolean variable to check if input document was read successfully
        ###### token - number of tokens in the input

    ###### Show input summary ######
    # col1, col2, col3=st.sidebar.columns(3) ###### Create columns
    # col1.markdown("###### :violet[#Tokens:] :blue["+str(st.session_state["token"])+"]") ###### Show number of tokens in the input
    # col2.write("###### :violet[#Words:] :blue["+str(st.session_state["words"])+"]") ###### Show number of words in the input
    # col3.markdown("###### :violet[#Embeddings:] :blue["+str(st.session_state["pages"])+"]") ###### Show number of embeddings in the input
    col1, col2 = st.sidebar.columns(2) ###### Create columns
    col1.markdown("###### :violet[#Tokens:] :blue["+str(st.session_state["token"])+"]") ###### Show number of tokens in the input
    col2.write("###### :violet[#Words:] :blue["+str(st.session_state["words"])+"]") ###### Show number of words in the input

    #### Splitting app into tabs ####
    tab1, tab2, tab3=st.tabs(["|__QnA__ 🔍|","|__Document Summary__ 📜|","|__About AnswerBot__ 🎭|"])

    with tab1: #### The QnA Tab
        
        if not st.session_state["succeed"]: ###### If input document was not read successfully, show error message
            st.error("#### The input document might be corrupted or the extraction of information from the input link failed. Try uploading a new document or entering a different link")
        else:
            initialize_chat("👋")  #### Initialize session state variables for the chat ####
            
            # If input is large, create embeddings for the document
            with st.spinner("Processing document..."):
                if (st.session_state["fn_db"] is None) and (st.session_state["token"] > 2000): 
                    if model_api == "OpenAI's GPT-3 [text-davinci-003]":
                        st.session_state["fn_db"] = create_embeddings(st.session_state["string_data"]) 
                    elif model_api == "Meta-Llama-2 [llama-2-7b-chat]":
                        fn_db = faiss_db_file_name(st.session_state["string_data"])
                        st.session_state["fn_db"] = fn_db

            #### Put user question input on top ####
            with st.form('input form', clear_on_submit=True):
                inp = st.text_input("Please enter your question below and hit Submit. Please note that this is not a chat, yet 😉", key="current")
                submitted = st.form_submit_button("Submit")

            if not submitted: #### This will render the initial state message by AnswerBot when no user question has been asked ####
                print(">>>>>> Rendering")

                with st.container(): #### Define container for the chat
                    render_chat() #### Function renders chat messages based on recorded chat history

            if submitted:
                #### This commented code block uses chatgpt model turbo-3.5 ####
                #### mdict=create_dict_from_session()
                #### if mdict !=[]:
                ####     response_text=q_response_chat(inp,info,mdict)
                ################################################################
                if st.session_state["token"]>2000:
                    with st.spinner("Finding relevant sections of the document..."):
                        info = search_context(st.session_state["fn_db"], inp, model_api)
                    with st.spinner("Preparing response..."):
                        final_text = llm_response(inp, info, model_api)
                else:
                    print("Step 3: ")
                    info = st.session_state["string_data"]
                    with st.spinner("Preparing response..."): #### Wait while openai response is awaited ####
                        final_text = llm_response(inp, info, model_api) #### Gets response to user question. In case the question is out of context, gets general response calling out 'out of context' ####
                
                    #### This section creates columns for two buttons, to clear chat and to download the chat as history ####
                col1,col2,col3,col4=st.columns(4)
                col1.button("Clear History",on_click=clear,type='secondary') #### clear function clears all session history for messages #####
                f=write_history_to_a_file() #### combines the session messages into a string ####
                col4.download_button("Download History",data=f,file_name='history.txt')

                with st.container():
                    chatbot(inp, final_text) #### adds the latest question and response to the session messages and renders the chat ####

    with tab2: #### Document Summary Tab ####
        if st.session_state["token"]>2000:
            with st.spinner("Finding most relevant section of the document..."):
                    # info=search_context(db,"The most important section of the document")
                    info=search_context(st.session_state["fn_db"], "The most important section of the document", model_api)
        else:
            info=st.session_state["string_data"]
        with st.form('tab2',clear_on_submit=False):
            choice=st.radio("Select the type of summary you want to see",("Summary","Talking Points","Sample Questions","Extracted Text"),key="tab2",horizontal=True)
            submitted=st.form_submit_button("Submit")
            if submitted:
                if choice=="Summary":
                    st.markdown("#### Summary")
                    st.write(summary(info, model_api))
                elif choice=="Talking Points":
                    st.markdown("#### Talking Points")
                    st.write(talking(info, model_api))
                elif choice=="Sample Questions":
                    st.markdown("#### Sample Questions")
                    st.write(questions(info, model_api))
                elif choice=="Extracted Text":
                    st.markdown("#### Extracted Text")
                    st.write(info)
            else:
                st.markdown("Note: :red[On the first time click, the app may go back to the QnA tab. Please click on the Document Summary tab again to see the response.]")
                

    with tab3:  #### About Tab #####
        # st.image(hline)
        col1, col2, col3,col5,col4=st.columns([10,1,10,1,10])

        with col1:
            first_column()
        with col2:
            st.write(" ")
        with col3:
             second_column()
        with col5:
            st.write(" ")
        with col4:
             third_column()
        # st.image(hline)
else: #### Default Main Page without Chat ####
    # st.image(hline)
    st.markdown("""<hr style="width:100%;height:3px;border:none;color:red;background-color:red;text-align:center" /> """, unsafe_allow_html=True)
    heads()
    st.markdown("""<hr style="width:100%;height:3px;border:none;color:red;background-color:red;text-align:center" /> """, unsafe_allow_html=True)
    # st.image(hline)
    col1, col2, col3,col5,col4=st.columns([10,1,10,1,10])
    with col1:
        first_column()
    with col2:
        st.write("")
        #st.image(vline,width=4)
    with col3:
        second_column()
    with col5:
        st.write("")
        #st.image(vline,width=4)
    with col4:
        third_column()
    # st.image(hline)
    st.markdown("""<hr style="width:100%;height:3px;border:none;color:red;background-color:red;text-align:center" /> """, unsafe_allow_html=True)

#### Contact Information ####
with st.sidebar.expander("📮 __Contact__"):
    # st.image(hline)
    contact()
    # st.image(hline)

#### Reset Button ####
if st.sidebar.button("🆘 Reset Application",key="Duo",use_container_width=True):
    for key in st.session_state.keys():
        del st.session_state[key]

    openai.api_key = None
    del os.environ["OPENAI_API_KEY"]
    
    st.experimental_rerun()

 






