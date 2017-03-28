import json 
import requests
import time
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ‘bot’))
os.environ.setdefault(“DJANGO_SETTINGS_MODULE”, bot.settings”)
from django.conf import settings

TOKEN = "326058249:AAF7nEaSHKvdXYWRY4Y56IFw7cF0HHKBdoo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    print("accessed API")
    response = requests.get(url)
    print("got response")
    content = response.content.decode("utf8")
    print(content)
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# Usa o offset para nao receber mensagens mais antigas que a do ID do offset
# Assim o get_updates nao traz todas as mensagens da conversa e apenas as mais novas
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

# Add a function that calculates the highest ID of all the updates we receive from getUpdates. 
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def create_message_to_send(text):
    message = ""
    if "oi" in text.lower():
        message = "Boa noite, mô fi!"
    else:
        message = text

    return message


def send_message(text, chat_id):

    # Modificando a mensagem que ele vai mandar
    message_text = create_message_to_send(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(message_text, chat_id)
    get_url(url)
    

def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        print("sending message")
        send_message(text, chat)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print("getting updates")
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()