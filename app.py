import os 
import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the environment
gemini_api_key = os.getenv('Google_api_key1')

# Lets configure the model
model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key = gemini_api_key)

# Design the UI of Application

st.title(":orange[HealthifyMe:] :blue[Your Personal Assistance]")
st.markdown('''
This application will assist you to get better and customized Health advice. 
You can ask your health related issues and get the personalized guidance.''')

st.write(
    '''Follow these steps:
* Enter your details in the sidebar.
* Rate your activity and fitness on the scale of 0-5.
* Submit your details.
* Ask your questions on the main page
* Click generate and relax.'''
)
# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name = st.sidebar.text_input('Enter your name')
gender = st.sidebar.selectbox('Select your gender',['Male','Female'])
age = st.sidebar.text_input('Enter your age')
weight = st.sidebar.text_input('Enter your weight in Kgs')
height = st.sidebar.text_input('Enter your height in Cms')
bmi = pd.to_numeric(weight)/((pd.to_numeric(height)/100)**2)
active = st.sidebar.slider('Rate your activity (0-5)',0,5,step=1)
fitness = st.sidebar.slider('Rate your fitness (0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name},your BMI is : {bmi} Kg/m^2")

# Lets use the gemini model tot generate the report
user_input = st.text_input('Ask me your question.')
prompt = f'''
<Role> You are an expert in health and wellness and has 10+ years experience in guiding people.
<Goal> Generate the customized report addressing the problem the user has asked. 
Here is the question that user has asked: {user_input}.
<Context> Here are the details that the user has provided.
name={name}
age={age}
gender={gender}
height={height}
weight={weight}
bmi={bmi}
activity rating (0-5)={active}
fitness rating (0-5)={fitness}

<Format> Following should be the outline of the report in the sequence provided below.
* Start with the 2-3 lines of comment on the details that user has provided.
* Explain what the real pproblem could be on the basis of input the user has provided.
* Suggest the possible reasons for the problem.
* What are the possible solutions?
* Mention the doctor from which specialization can be visited if required.
* In last create a final summary of all the things that have been discussed in the report.

<Instructions> 
* use bullet points wherever possible.
* create tables to represent data wherever possible.
* Strictly avoid prescribing any medicine.
'''

if st.button('Generate'):
    response= model.invoke(prompt)
    st.write(response.content)
