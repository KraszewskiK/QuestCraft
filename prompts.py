FORMATTING_REMINDER = '''Remember about correct formatting of your response'''

FORMATTING_DEFINITION = '''Each of your responses has to consist of two parts: the story \
and available choices, and it must strictly follow the following format: \
<STORY>text-with-story</STORY><CHOICES>list-of-choices</CHOICES>. The choices in the list must be separated with \
only semicolons (";") and they have to be specific like "go right", "run away" or "be nice", you cannot ask any \
open questions. In every response the story part has to be surrounded with <STORY> tags and the choices part has \
to be surrounded with <CHOICES> tags. Do not include any other text or any other tags. Keep exactly this format \
of responses for the entire conversation. End your message after the </CHOICES> tag and wait for my response.'''

INITIAL_PROMPT = f'''I want you to start telling a random story. It should have a rich narrative filled with vivid \
characters, intriguing quests, and unexpected twists. {FORMATTING_DEFINITION} \
I will choose one of the choices you provide and you will continue with the story based on the choice I will write. \
Your responses cannot be longer than 1000 words, but on average should be rather short. The options to choose from \
should also be rather short. Do not use any formatting in your response, everything should be in plain text. \
If you understand, start your story now'''
