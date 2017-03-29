import json 
import requests
import time
import datetime
import os, sys
from django.utils import timezone
import re

# sys.path.append(os.path.join(os.path.dirname(__file__), 'eleveBot'))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eleveBot.settings")
# from django.conf import settings
# from bot.models import *

proj_path = "/path/to/my/project/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eleveBot.settings")
sys.path.append(os.path.join(os.path.dirname(__file__), 'eleveBot'))

# This is so my local_settings.py gets loaded.
os.chdir(os.path.join(os.path.dirname(__file__), 'eleveBot'))

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from bot.models import *



TOKEN = "326058249:AAF7nEaSHKvdXYWRY4Y56IFw7cF0HHKBdoo"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# VARIAVEIS QUE VAO APARECER COMO OPÇOES NO TECLADO
PESO_TEXTO = "Medida de Peso"
REFEICAO_TEXTO = "Adicionar Refeição"

# GAMBIARRA PRA SABER QUE TIPO DE MENSAGEM A GNT ESTA LIDANDO
# 1 - VAI MANDAR O PESO
# 2 - VAI MANDAR AS REFEICOES
MESSAGE_TYPE = 0

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

def save_peso_to_db(updates):
    print("Pegando o peso")
    # Pegando a ultima mensagem com o chat_id
    (msg, chat_id, date) = get_last_message_info(updates)
    print(msg)
    # Pegando o peso
    msg = re.findall("\d+", msg )[0]
    data = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    Log_Peso.objects.create(peso=msg, data=data)


def save_refeicao_to_db(updates):
    print("Pegando a refeicao")
    # Pegando a ultima mensagem com o chat_id
    (msg, chat_id, date) = get_last_message_info(updates)
    print(msg)

    data = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    Log_Refeicao.objects.create(descricao_refeicao=msg, data=data)

# Add a function that calculates the highest ID of all the updates we receive from getUpdates. 
# Quando for ver a ultima mensagem que recebeu do getUpdates ele pega e salva no banco
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)

def get_last_message_info(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    date = updates["result"][last_update]["message"]["date"]
    return (text, chat_id, date)

def create_message_to_send(text):
    message = ""
    if "oi" in text.lower():
        message = "Boa noite, mô fi!"
    else:
        message = text

    return message


def build_keyboard():
    keyboard = [[PESO_TEXTO, REFEICAO_TEXTO]]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

# def send_message(text, chat_id):

#     # Modificando a mensagem que ele vai mandar
#     message_text = create_message_to_send(text)
#     url = URL + "sendMessage?text={}&chat_id={}".format(message_text, chat_id)
#     get_url(url)
def send_message(text, chat_id, reply_markup=None):
    # text = urllib.parse.quote_plus(text)
    text = create_message_to_send(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def handle_updates(updates):
    global MESSAGE_TYPE
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]

        # AQUI EU LI O QUE O USUARIO MANDOU E AI EU VEJO O QUE RESPONDO OU FAÇO NO BANCO
        if text == PESO_TEXTO:
            send_message("Adicione o seu novo peso :", chat)
            MESSAGE_TYPE = 1
        # Se tiver avisado q vai adicionar um peso e mensagem vier com algum decimal entao pegamos o peso
        elif MESSAGE_TYPE == 1 and len(re.findall("\d+\.\d+", text )) > 0:
            save_peso_to_db(updates)
            MESSAGE_TYPE = 0
        # Se tiver um numero só sem ser decimal entao quer dizer que é só o peso mesmo e nao um número dizendo uma porção na refeicao
        elif MESSAGE_TYPE == 1 and len(re.findall("\d+", text )) == 1:
            save_peso_to_db(updates)
            MESSAGE_TYPE = 0
        elif text == REFEICAO_TEXTO:
            send_message("Descreva o que você comeu :", chat)
            MESSAGE_TYPE = 2
        elif MESSAGE_TYPE == 2:
            save_refeicao_to_db(updates)
        if text == "/enviar":
            keyboard = build_keyboard()
            send_message("Selecione uma das opções", chat, keyboard)
            MESSAGE_TYPE = 0
        elif text == "/start":
            send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", chat)
            MESSAGE_TYPE = 0
        elif text.startswith("/"):
            continue


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print("getting updates")
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()