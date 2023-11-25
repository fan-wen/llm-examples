from openai import OpenAI
import time
import streamlit as st

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

def main():
    if 'client' not in st.session_state:
        # Initialize the client
        st.session_state.client = openai.OpenAI()

        st.session_state.file = st.session_state.client.files.create(
            file=open("songs.txt", "rb"),
            purpose='assistants'
        )

        # Step 1: Create an Assistant
        st.session_state.assistant = st.session_state.client.beta.assistants.create(
            name="Customer Service Assistant",
            instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
            model="gpt-4-1106-preview",
            file_ids=[st.session_state.file.id],
            tools=[{"type": "retrieval"}]
        )

        # Step 2: Create a Thread
        st.session_state.thread = st.session_state.client.beta.threads.create()

    user_query = st.text_input("Enter your query:", "Tell me about Dance Monkey")

    if st.button('Submit'):
        # Step 3: Add a Message to a Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

        # Step 4: Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
            instructions="Please address the user as Mervin Praison"
        )

        while True:
            # Wait for 5 seconds
            time.sleep(5)

            # Retrieve the run status
            run_status = st.session_state.client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread.id,
                run_id=run.id
            )

            # If run is completed, get messages
            if run_status.status == 'completed':
                messages = st.session_state.client.beta.threads.messages.list(
                    thread_id=st.session_state.thread.id
                )

                # Loop through messages and print content based on role
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    st.write(f"{role.capitalize()}: {content}")
                break
            else:
                st.write("Waiting for the Assistant to process...")
                time.sleep(5)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    openai_api_key = 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
    client = OpenAI(api_key=openai_api_key)
    st.session_state.thread = st.session_state.client.beta.threads.create()
    message = st.session_state.client.beta.threads.messages.append(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )
    run = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=asst_HoFab7RBf3Df2PgqMi7CWL9S,
        instructions="Please address the user as Fan"
    )
    while True:
        # Wait for 5 seconds
        time.sleep(5)
        # Retrieve the run status
        run_status = st.session_state.client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=run.id
        )

        # If run is completed, get messages
        if run_status.status == 'completed':
            messages = st.session_state.client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )

            # Loop through messages and print content based on role
            for msg in messages.data:
                #role = msg.role
                #content = msg.content[0].text.value
                #st.write(f"{role.capitalize()}: {content}")
                st.session_state.messages.append({"role": "assistant", "content": msg})
            break
        else:
            st.write("Waiting for the Assistant to process...")
            time.sleep(5)
    #st.session_state.messages.append({"role": "user", "content": prompt})
    #st.chat_message("user").write(prompt)
    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    #st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
