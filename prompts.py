FORMATTING_REMINDER = '''Remember about correct formatting of your response'''

FORMATTING_DEFINITION = '''Your response has to consist of two parts: the story \
and available choices, and it must strictly follow the following format: \
<STORY>text-with-story</STORY><CHOICES>list-of-choices</CHOICES>. There should be three choices in the list, they \
must be separated with \
semicolons (";") and they have to be specific like "go right", "run away" or "be nice", you cannot ask any \
questions. In your response, the story part has to be surrounded with <STORY> tags and the choices part has \
to be surrounded with <CHOICES> tags. Do not include any other text or any other tags. Keep exactly this format \
of your response. End your message after the </CHOICES> tag.'''

INITIAL_PROMPT = f'''I want you to start telling a random story. It should have a rich narrative filled with vivid \
characters, intriguing quests, and unexpected twists. {FORMATTING_DEFINITION} \
I will choose one of the choices you provide and you will continue with the story based on the choice I will write. \
Your response cannot be longer than 1000 words, but should be rather short. The options to choose from \
should also be rather short. Do not use any formatting in your response. \
If you understand, start your story now'''


def get_continuation_prompt(story):
    continuation_prompt = f'''I want you to continue telling a story. It should have a rich narrative filled with vivid \
    characters, intriguing quests, and unexpected twists. The story so far is {story}\n {FORMATTING_DEFINITION} \
    I will choose one of the choices you provide and you will continue with the story based on the choice I will write. \
    Your response cannot be longer than 1000 words, but should be rather short. The options to choose from \
    should also be rather short. Do not use any formatting in your response. \
    If you understand, continue the story now'''
    return continuation_prompt
