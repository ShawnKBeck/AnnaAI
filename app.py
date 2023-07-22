import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize an empty list of messages
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

# Display all previous messages
for message in st.session_state['messages']:
    st.write(f"{message['role']}: {message['content']}")

# Input for the new user message
new_message = st.text_input("Your message")

# When the user presses the send button, add their message to the list and generate a response
if st.button("Send"):
    st.session_state['messages'].append({"role": "user", "content": new_message})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state['messages'],
        temperature=1,
        max_tokens=256
    )

    st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message['content']})

    # Clear the text input
    st.empty()
