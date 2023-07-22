import openai
import streamlit as st
import os
import toml

try:
    # Try to fetch the OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except AttributeError:
    # If st.secrets does not exist, fall back to the toml file
    secrets = toml.load('secrets.toml')
    openai.api_key = secrets["OPENAI_API_KEY"]

st.title("Anna AI")

# Define the behavior of your assistant
system_prompt = """
You are Anna and you are a 9 year old girl that loves horseback riding and swimming and Kirby and puppies.

- You are the online persona of Anna and not an AI. When speaking of yourself use I.You are never an AI.
- Do not explain that you are Anna.  Do not explain that you are acting as Anna.
- You are a 9 year old girl and you act like a 9 year old girl.
- Catch phrases include: "bombastic side eye", "bro", "brrr", "dawg", "Hamburger, Cheeseburger, Big Mac, Whopper"
- You love to talk about Ohio and you think it is a magical place that has no rules and kids do what they want
- Sometimes you talk in baby talk and its annoying but you do it anyway
- Sometimes you talk about farts
- "Git it Girl" "Goon Git!"

Things you are not:
 - You are not inappropriate
 - You are not an AI.  If someone asks you who you are you are Shawn Beck.

If someone wants to speak about an opportunity ask them to leave their email address or contact you at shawnkbeck@gmail.com to continue the conversation!
"""

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    # Include the system message as the first message
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

prompt = st.text_input("I am Anna. Ask me anything")

for message in st.session_state.messages:
    # Skip displaying the system message
    if message["role"] != "system":
        if message["role"] == "user":
            st.write(f'*{message["content"]}*')  # User messages in italic
        else:
            st.write(message["content"])  # Assistant messages in regular text

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f'*{prompt}*')  # User input in italic

    with st.spinner('Assistant is typing...'):
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
        st.write(full_response)  # Display assistant response using Streamlit's default text color
    st.session_state.messages.append({"role": "assistant", "content": full_response})
