import requests
import streamlit as st

st.set_page_config(page_title="iLang | Playground", layout="wide")
st.header(':red[iLang Playground]')
st.caption("Powered by Phi-3 | :rainbow[Microsoft]")


def chat(text):
    api_url = "http://10.10.31.55:8070/chat"
    response = requests.post(api_url, json={"text": text})
    return response.json()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message GenAI..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner('Thinking...'):
        response = chat(prompt)['output']
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
