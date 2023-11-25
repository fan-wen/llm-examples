from openai import OpenAI
import openai
import time
import streamlit as st

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    st.session_state.client = openai.OpenAI(api_key=openai_api_key)
    st.session_state.thread = st.session_state.client.beta.threads.create()
    message = st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )
    run = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id = "asst_HoFab7RBf3Df2PgqMi7CWL9S",
        tools = ["retrieval"],
        instructions = "Please address the user as Fan"
    )
    while True:
        # Wait for 5 seconds
        time.sleep(5)
        # Retrieve the run status
        run_status = st.session_state.client.beta.threads.runs.retrieve(
            thread_id = st.session_state.thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id = st.session_state.thread.id
            )
            # Loop through messages and print content based on role
            last_msg = messages.data[0].content[0].text.value
            st.chat_message("assistant").write(last_msg)
            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                #st.write(f"{role.capitalize()}: {content}")
                st.session_state.messages.append({"role": "assistant", "content": content})
            break
        else:
            #st.write("Waiting for the Assistant to process...")
            time.sleep(5)
    #st.session_state.messages.append({"role": "user", "content": prompt})
    #st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    #st.chat_message("assistant").write(msg)
