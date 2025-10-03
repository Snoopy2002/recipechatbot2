# -*- coding: utf-8 -*-

#https://docs.streamlit.io/
import streamlit as st
from openai import OpenAI
import os
import time

questions=list()
responses=list()
messages=list()

def getkey(): #to run on streamilt and get secrets info
    key = st.secrets["OPENAI_API_KEY"] #get from streamlit secrets file
    email=st.secrets["email"]
    pwd=st.secrets["emailpwd"]
    return(key,email,pwd)
    
def getkeylocal(): #for local execution
    f=open('appkeys.txt','r')
    key=f.readline()
    email=f.readline()
    emailpwd=f.readline()
    return(key,email, emailpwd)
   

def sendmail(rq, email, emailpwd): #sends an email using yagmail with a passed file as a file attachment and the original recipe request to use in the body
    import yagmail #https://pypi.org/project/yagmail/  #https://github.com/kootenpv/yagmail?tab=readme-ov-file#attaching-files
    dest=input("Enter your destination email: ")
    try:
      receiver = dest
      body = rq
      yag = yagmail.SMTP(email, emailpwd)
      yag.send(to=receiver, subject="Your requested recipe file from ChatGPT", contents=body)

    except Exception as E:
      print(E)
      print("Error, unable to create email.")
      return(False)
    else:
      return(True)


def providerecipe(recipequestion,email,pwd):
    
       recipes=0
       system_prompt='You are an experienced cook.  Provide me with your best suggestion for the requested recipe based on your experience and knowledge.'

       messages.append({'role':'system','content':system_prompt})
       messages.append({'role':'user', 'content': recipequestion})
       n=2 #number of recipes returned
       botresponse=client.chat.completions.create(model='gpt-3.5-turbo', messages=messages,n=n,temperature=1.6,presence_penalty=1.0)
       progress_text = "Recipe generation in progress. Please wait."
       my_bar = st.progress(0, text=progress_text)
    
       for percent_complete in range(100):
          time.sleep(0.1)
          my_bar.progress(percent_complete + 1, text=progress_text)
       time.sleep(1)
       my_bar.empty()
       
       
       recipes=len(botresponse.choices)
       with st.chat_message("assistant"):
         for i in range(0,recipes):
            st.subheader(f"Recipe {i+1}",divider=True)
            st.write(botresponse.choices[i].message.content)
            responses.append(botresponse.choices[i].message.content)
            questions.append(recipequestion)
            print("\n" + '*' * 50 + "\n")
           
            status=sendmail(recipequestion, email, pwd)
            if status == True:
              print("Email with recipe sent successfully!")


           
     

def init_existing_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    #for message in st.session_state["messages"]:
     #   with st.chat_message(message["role"]):
     #       st.markdown(message["content"])

        
def addrecipe(request):
    
    if request:
       st.session_state["messages"].append({"role": "user", "content": request})
       with st.chat_message("user"):
           st.markdown(request)


if __name__ == '__main__':
    key,email, pwd=getkey()
    #key,email,emailpwd=getkeylocal() #to run on local machine
    os.environ["OPENAI_API_KEY"]=key
    os.getenv('OPENAI_API_KEY')
    client=OpenAI() #can also pass key to client if enviro vbl not set

    col1,col2=st.columns([0.80,0.20]) #set the page columns
    with col1:
        st.subheader('Welcome to the ChatGPT Recipe Chatbot!', divider='violet') #create the header
        
    with col2:
        st.image("recipesfromchatgpt.png") #import i mage
    init_existing_messages() #initialize responses
    with st.container(border=True):
      reciperequest = st.chat_input("Ask me for a recipe. ")
      if reciperequest:
        addrecipe(reciperequest)
        providerecipe(reciperequest, email, pwd)

    

