import json
from json import JSONDecodeError

import streamlit as st
from hugchat import hugchat

import prompts
import utils

# Streamlit page configuration
st.set_page_config(
    page_title="TaleMancer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://github.com/KraszewskiK/TaleMancer/issues",
        'About': '''## About TaleMancer

TaleMancer is an interactive RPG app that allows you to embark on captivating storytelling adventures. Shape the story through your choices and immerse yourself in a world of epic quests and mystical encounters.

With the power of a large language model, TaleMancer generates dynamic narratives that respond to your decisions. Every choice you make influences the plot, characters, and outcomes, giving you a personalized and engaging gameplay experience.

Whether you seek thrilling battles, mysterious puzzles, or deep character interactions, TaleMancer offers multiple story arcs and questlines for you to explore. Each playthrough offers a unique journey, with consequences and endings that reflect the paths you choose.

Get ready to unleash your imagination and become the master of your own tale in TaleMancer!

Start your adventure now and let the stories unfold!

---

**Note:** TaleMancer is developed using Streamlit, an open-source framework for building interactive web applications with Python. It utilizes the power of a large language model to deliver an immersive RPG experience.
'''
    }
)

# Load cookies
cookies = json.loads(st.secrets['cookies'])
# Create the chatbot instance
if 'chatbot' not in st.session_state:
    st.session_state['chatbot'] = hugchat.ChatBot(cookies=cookies)
    st.session_state['chat_id'] = st.session_state['chatbot'].get_conversation_list()[-1]
    st.session_state['conversation'] = {st.session_state['chat_id']: {'prompts': [], 'responses': []}}
chatbot = st.session_state['chatbot']
chat_id = st.session_state['chat_id']

# Page design
with st.sidebar:
    if st.session_state['conversation'][chat_id]['responses']:
        if st.button('Start a new story'):
            # Create a new conversation
            st.session_state['chat_id'] = chatbot.new_conversation()
            chatbot.change_conversation(st.session_state['chat_id'])
            st.session_state['conversation'][st.session_state['chat_id']] = {'prompts': [], 'responses': []}

    st.title('🎮📚🔮TaleMancer RPG storyteller')
    st.markdown('''
        ## About
        This is an LLM-powered app built using:
        - [Streamlit](https://streamlit.io/)
        - [HugChat](https://github.com/Soulter/hugging-chat-api)
        - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) Large Language Model

        💡 Note: No API key required!
        ''')
    st.write('Made by [KraszewskiK](https://github.com/KraszewskiK)')

st.write("## Welcome to the TaleMancer app! Get ready to begin your adventure!")


# get model's response, put prompt and response in session_state
def get_response(prompt):
    with st.spinner('Writing the story'):
        st.session_state['conversation'][chat_id]['prompts'].append(prompt)
        story, choices = utils.generate_response(chatbot, prompt, chat_id, cookies[0])
        st.session_state['conversation'][chat_id]['responses'].append((story, choices))
    # if add_id_message['status'] != 200 or preserve_context_message['status'] != 200:
    #     st.error(f'{add_id_message["message"]} \n {preserve_context_message["message"]}')


if not st.session_state['conversation'][chat_id]['prompts']:
    start_story = st.button('Start your story')
    if start_story:
        get_response(prompts.INITIAL_PROMPT)

# write the previous responses and prompts
for i, response in enumerate(st.session_state['conversation'][chat_id]['responses']):
    st.write(response[0])
    # write stories and chosen options until the last response
    if i != len(st.session_state['conversation'][chat_id]['responses']) - 1:
        st.write(st.session_state['conversation'][chat_id]['prompts'][i + 1])
        st.divider()
    else:  # for the last response create buttons for each choice
        choices_buttons = [None] * len(response[1])
        for j, choice in enumerate(response[1]):
            # after clicking the button create a prompt based on the choice
            choices_buttons[j] = st.button(choice, on_click=lambda: get_response(choice))
