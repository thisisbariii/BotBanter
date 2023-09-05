import openai
import streamlit as st
from streamlit_chat import message

# Set your OpenAI API key (preferably from an environment variable)
openai.api_key = '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'

# Initialize Streamlit session_state variables
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def generate_response(prompt):
    st.session_state['prompts'].append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['prompts']
    )
    
    response = completion.choices[0].message.content
    return response

def reset_chat():
    st.session_state['prompts'] = [{"role": "system", "content": "You are a helpful assistant. Answer as concisely as possible with a little humor expression."}]
    st.session_state['past'] = []
    st.session_state['generated'] = []

def chat_click():
    user_input = st.session_state['user']
    if user_input:
        output = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['prompts'].append({"role": "assistant", "content": output})
    st.session_state['user'] = ""

# Use a placeholder image URL for your logo
st.image("https://api.dicebear.com/5.x/bottts/svg?seed=88", width=80)
st.title("BotBanter")

user_input = st.text_input("You:", key="user")
chat_button = st.button("Send", on_click=chat_click)
end_button = st.button("New Chat", on_click=reset_chat)

if st.session_state['generated']:
    for i, (user_msg, generated_msg) in enumerate(zip(st.session_state['past'], st.session_state['generated'])):
        tab1, tab2 = st.tabs(["normal", "rich"])
        with tab1:
            message(generated_msg, key=str(i))
        with tab2:
            st.markdown(generated_msg)
        message(user_msg, is_user=True, key=str(i) + '_user')
        
        
        
