import requests
import urllib3
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable warnings
urllib3.disable_warnings(InsecureRequestWarning)

with open("/opt/airflow/src/open_ai_call/secrets.yaml") as f:
    secrets = yaml.safe_load(f)

api_key = secrets["openai"]["api_key"]

message = 'Hi! how are you doing?'


def basic_gpt_response(message, api_key):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
    }

    data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": message}
    ]
    }   

    # Send the POST request
    response = requests.post(url, headers=headers, json=data, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        response_data = response.json()
        
        # Extract the message content
        message_content = response_data['choices'][0]['message']['content']
        print("AI says:", message_content)
    else:
        print("Failed to get a valid response", response.status_code, response.text)
        message_content = None
    
    return message_content

if __name__ == '__main__':

    message = 'Hi! how are you doing?'
    for x in range(5):
        message=basic_gpt_response(message, api_key)
        