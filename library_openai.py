import configparser
import requests
import shutil
import openai
import platform
# from library_utils import json_pretty

if platform.system() == 'Windows':
    creds_file = 'C:\\Users\\JO008BU\\OneDrive - Pitney Bowes\\Data.Analytics\\OTC_OR_VM\\creds.ini'
    import os
    os.environ['REQUESTS_CA_BUNDLE'] = "C:\\Users\\JO008BU\\OneDrive - Pitney Bowes\\Data.Analytics\\Automations\\Zscaler Root CA.crt"
else:
    creds_file = '/home/admin.eng/creds.ini'

config = configparser.ConfigParser()
config.read(creds_file)
API_KEY = config['OPENAI']['secret_key']
openai.api_key = API_KEY

CONTENT_TYPE = "application/json"
API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
# API_BASE_ENDPOINT = 'https://graph.microsoft.com/v1.0'
# GRAPH_API_BETA_ENDPOINT = 'https://graph.microsoft.com/beta'

headers = {
        "Accept": CONTENT_TYPE,
        "Authorization": f"Bearer {API_KEY}"
    }

MODELS = {
    "gpt-4": 8192,
    "gpt-3.5-turbo-16k": 16384
}


def num_tokens_from_string(string, encoding_name="cl100k_base"):
    import tiktoken
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def send_chat(message, choices=1, temperature=0.2, model="gpt-4"):
    json_body = {
      "model": model,
      "messages": [{"role": "user", "content": message}],
      "temperature": temperature
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=json_body)
    if response.status_code == 200:
        resp_json = response.json()
        if 'choices' in resp_json:
            if choices == 1:
                chat_response = resp_json['choices'][0]['message']['content'].encode().decode('unicode_escape').replace('"', '')
            else:
                # TODO - at some point may want to have different choices for responses
                chat_response = 'NOT CONFIGURED FOR MULTIPLE CHOICES'
            return chat_response
        else:
            print(f'"choices" not in response json, here\'s the payload:\n{resp_json}')
            raise ValueError("OpenAI API call failed, failing the script so chat programs don't say they didn't understand")
            # return False

        # {
        #     "id": "chatcmpl-77QvxRj7UDadNCVKKgLJpmlrgccKv",
        #     "object": "chat.completion",
        #     "created": 1682006185,
        #     "model": "gpt-3.5-turbo-0301",
        #     "usage": {
        #         "prompt_tokens": 56,
        #         "completion_tokens": 62,
        #         "total_tokens": 118
        #     },
        #     "choices": [
        #         {
        #             "message": {
        #                 "role": "assistant",
        #                 "content": "Hey Alex! Guess what? Your request for account '0012345678 CUSTOMER NAME' has just been updated to be fully bank compliant! That means you're one step closer to closing this deal and becoming a top-performing sales rep! Keep up the great work and let's seal the deal today!"
        #             },
        #             "finish_reason": "stop",
        #             "index": 0
        #         }
        #     ]
        # }

    else:
        print(f'i got back status code of {response.status_code} and payload was:\n{response.json()}')
        return False


def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream=True)
    if image_res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print('ERROR LOADING IMAGE')

    return image_res.status_code


def generate_image(image_prompt, file_name, size='256x256'):
    response = openai.Image.create(
        prompt=image_prompt,
        # prompt='meme of a happy and funny animal and the caption says "now i can do my happy dance"',
        n=1,
        size=size #'1024x1024'
    )
    image_url = response['data'][0]['url']
    save_response = save_image(image_url, file_name)
    return save_response


def get_completion_from_messages(messages, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]



# response = openai.Completion.create(
#   model="gpt-3.5-turbo",
#   prompt="Human: Can you write a brief upbeat email to a sales rep named Alex telling Alex that account '0017427993 UTILITY LAB SERVICES' has been updated to bank compliant and encourage them to close the sales deal?\nAI:",
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0.0,
#   presence_penalty=0.6,
#   stop=[" Human:", " AI:"]
# )
# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="\n\nInstall at Address Details 2990590 INACTIVE in OLFM for the customer account id :1919271 for the contract :0041331369/Atleast one contract lines record failed validation for the contract :0041331369Tl;dr",
#   temperature=0.7,
#   max_tokens=60,
#   top_p=1.0,
#   frequency_penalty=0.0,
#   presence_penalty=1
# )