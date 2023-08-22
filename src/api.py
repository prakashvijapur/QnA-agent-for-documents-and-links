'''
api.py contains all functions related to reading the OpenAI API key and checking if it is valid
'''


import openai ###### Import OpenAI library
import streamlit as st ###### Import Streamlit library
import os ###### Import os library for environment variables
from configparser import ConfigParser ###### Import ConfigParser library for reading config file to get model
import requests
import json

#### Create config object and read the config file ####
config_object = ConfigParser() ###### Create config object
config_object.read("./config.ini") ###### Read config file
model=config_object["MODEL"]["openai_model"] ##### model for GPT call

#### Check if OpenAI API key is present ####
#### this function checks if the key is present in the environment variables or in the .env file ####
#### if not present, it asks the user to input the key ####
#### if present, it checks if the key is valid ####
#### if not valid, it asks the user to input the key ####
#### if valid, it returns True ####
#### if not present, it returns False ####
#### if present but not valid, it returns False ####
def check_key(): 
    """
        The function checks if the user has provided any API key in the input box.
    """
    
    if st.session_state["api_key"] is not None: 
        st.sidebar.info("API key detected")
        return True 
    
    # Not required in current setup ---------------------------------------------------
    # elif os.path.exists(".venv") and os.environ.get("OPENAI_API_KEY") is not None:
    #     openai.api_key=os.environ["OPENAI_API_KEY"] 
    #     if validate_key(): 
    #         st.sidebar.success("API key loaded from .env", icon="🚀")
    #         return True ###### If key is present, return True
    #     else:
    #         del os.environ['OPENAI_API_KEY']
    #         openai.api_key=None
    #         input_key()
    #         if openai.api_key:
    #             return True
    #         else:
    #             return False
    # ---------------------------------------------------------------------------------

    else:
        input_key()
        if st.session_state["api_key"] is not None:
            return True
        else:
            return False
    
def validate_key(model_api):
    try:
        # Note: model api can either be "OpenAI's GPT-3 [text-davinci-003]" or "Meta-Llama-2 [llama-2-7b-chat]"
        
        if model_api == "OpenAI's GPT-3 [text-davinci-003]":
            openai.api_key = st.session_state["api_key"]
            os.environ["OPENAI_API_KEY"] = st.session_state["api_key"]
            r = openai.Completion.create(model=model, prompt="t.", max_tokens=5)
            print("Connect to OpenAI API.")
        elif model_api == "Meta-Llama-2 [llama-2-7b-chat]":
            response = requests.post(st.session_state["api_key"]+"health-check")
            response = json.loads(response.content)["status"]
        
            if response == 'RUNNING':
                print("The FastAPI application is running.")
            else:
                print("The FastAPI application is not running.")
        
        st.sidebar.success("API key validated")
        return True
        
    except:
        st.sidebar.error("API key invalid for {}, please change the key".format(model_api))
        return False
    
def clear_key():
    st.session_state["api_key"] = None
    del os.environ["OPEN_API_KEY"]

def input_key():
    st.session_state["api_key"] = None

    with st.sidebar.form("API",clear_on_submit=True):
            api_key=st.text_input("Please enter your API key",type='default')
            submit = st.form_submit_button("Enter")
    if submit:
        st.session_state["api_key"] = api_key
        check_key()



