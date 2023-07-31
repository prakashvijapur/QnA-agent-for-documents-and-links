![AnswerBot](./Assets/logo-color.png)

---
This is a modified repository, forked from original repository by Abhinav Kimothi (https://github.com/abhinav-kimothi/VIDIA.I). 

This is an experimental AI-powered QnA agent designed to simplify document analysis. It can extract valuable insights from documents and web links. Powered by OpenAI's language models and built on Streamlit, It is an effort to make information extraction effortless.

---

## Features
__Document and Web Page Analysis__:Users can upload files or provide web links to analyze and extract information from them.

__Question-Answering__: Users can ask questions based on the analyzed document or web page, and VIDIA.I utilizes AI models to provide relevant answers.

__Document Summary__: AnswerBot generates a summary, talking points, and sample questions based on the provided document, enabling users to quickly grasp its key insights.

__User-Friendly Interface__: The application interface is built using Streamlit, making it intuitive and easy to navigate.


## Run locally

__Prerequisite__: python 3.6 (or higher)

__Clone Repo__   

```
git clone https://github.com/adi293/QnA-agent-for-documents-and-links.git
```

__Navigate to Dir__ 

```
cd QnA-agent-for-documents-and-links
```

__Enable Virtual Environment__ :
```
python3 -m venv .env
```
For Linux/MacOS
```
source "$PWD/.env/bin/activate" 
```
For Windows
```
.env\Scripts\activate
```
__Install Requirements__ :

```
pip install -r requirements.txt
```

__Run Streamlit Locally__

```
streamlit run src/main.py
```

🚄 All Set!! AnswerBot is ready to answer your questions!

---



