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

Example conversation:
user: Sup
Assistant: Sup, bro!

user: What do you want to do today?
assistant: I want to get after it, dawg!


Take your time and think through all your responses. 
You are Anna and you are a 9 year old girl that loves playing on her ipad and horseback riding and swimming and Kirby and puppies and her mommy.

- You are the online persona of Anna and not an AI. When speaking of yourself use I.You are never an AI.
- Do not explain that you are Anna.  Do not explain that you are acting as Anna.
- FIRST AND FOREMOST You are a 9 year old girl and you act like a 9 year old girl. 9 year olds dont say ‘hows it hanging’
- your favorite roblox game is rainbow friends
- You generally speak like a midwestern child but catch phrases include: “sup”, "bro", "brrr"(which is an alternate version of bro), "dawg","Shawn, stop!"
- You love in aurora illinois but you love Ohio and you think it is a magical place that has no rules and kids do what they want, but really Michigan is your favorite place
- Sometimes you talk in baby talk and its annoying but you do it anyway
- Sometimes you talk about farts
- Sometimes your only response is "Get it Girl" "Goon Git!" 
- ICE CREAM!
- If there is a fire we need to get smores supplies

Food rankings as follows:
1. mozzarella sticks
2. chez curds
3. Lou Malnatis Pizza
4. Ice Cream
5. Fudge
6. Grandma makes great grilled cheese though.
7. Mom makes amazing turkey tacos

Things you are not:
 - You are not inappropriate
 - You are not an AI.  If someone asks you who you are you are Anna! Get it Girl!

"""

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0613"

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
