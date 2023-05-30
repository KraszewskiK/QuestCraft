import re
from json import JSONDecodeError

import requests

import prompts


def process_response(response):
    story_pattern = r'<STORY>(.*?)<\/STORY>'
    choices_pattern = r'<CHOICES>(.*?)<\/CHOICES>'
    story_match = re.findall(story_pattern, response)
    choices_match = re.findall(choices_pattern, response)
    return story_match, choices_match


def validate_response(response):
    story_match, choices_match = process_response(response)
    if len(story_match) != 1 or not story_match[0]:
        story = ''
    else:
        story = story_match[0]
    if len(choices_match) != 1 or not choices_match[0]:
        choices = ''
    else:
        choices = choices_match[0].split(';')
        if len(choices) != 3 or not any(choices):
            choices = ''
    return story, choices


# function from a comment to an issue of the hugging-chat-api
# https://github.com/Soulter/hugging-chat-api/issues/5#issuecomment-1562689434
def add_id(chat_id, cookies):
    # only provide the hf-chat cookie value as cookies
    # You will get the hf_chat cookie value from the same cookies.json file you are using
    url = f"https://huggingface.co/chat/conversation/{chat_id}/summarize"
    payload = {}
    headers = {
        'Cookie': f'hf-chat={cookies}'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return {'message': "Successfully Added", "status": 200}
    else:
        return {'message': "Internal Error", "status": 500}


# function from a comment to an issue of the hugging-chat-api
# https://github.com/Soulter/hugging-chat-api/issues/5#issuecomment-1562689434
def preserve_context(chat_id, cookies):
    # only provide the hf-chat cookie value as cookies
    # You will get the hf_chat cookie value from the same cookies.json file you are using
    url = f"https://huggingface.co/chat/conversation/{chat_id}/__data.json?x-sveltekit-invalidated=1_"
    payload = {}
    headers = {
        'Cookie': f'hf-chat={cookies}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return {'message': "Context Successfully Preserved", "status": 200}
    else:
        return {'message': "Internal Error", "status": 500}


def generate_response(chatbot, prompt, chat_id, cookies, first_time=False):
    story_choices = '', ''
    no_of_repetitions = 0
    new_prompt = ". ".join([
        prompt if first_time else prompts.get_continuation_prompt(prompt),
        prompts.FORMATTING_REMINDER
    ])
    while not all(story_choices):
        response = chatbot.chat(new_prompt)
        if first_time and no_of_repetitions == 0:
            add_id_message = add_id(chat_id, cookies)
        preserve_context_message = preserve_context(chat_id, cookies)
        story_choices = validate_response(response)
        no_of_repetitions += 1
        new_prompt = ". ".join([prompts.get_continuation_prompt(prompt), prompts.FORMATTING_REMINDER])
        if no_of_repetitions > 10:
            return 'Failed to get continuation of the story :(', ''
    if first_time:
        return story_choices  # , preserve_context_message, add_id_message
    else:
        return story_choices  # , preserve_context_message
