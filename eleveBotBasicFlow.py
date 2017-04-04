import time
import telepot
import messages
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import json

state = {}


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    first_name = msg['from']['first_name']

    # will be sent in the end of this method
    message = None
    markup = None

    # markup = InlineKeyboardMarkup(inline_keyboard=[
    #               [InlineKeyboardButton(text='Press me', callback_data='press')],
    #           ])
    #
    #   bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

    if chat_id not in state:

        # Hi fulano
        message_tmp = messages.MessageHelloName(first_name)
        bot.sendMessage(chat_id, message_tmp.get_text())

        # Say "hi" to start recording
        message = messages.MessageSayHi()

    else:
        if isinstance(state[chat_id], messages.MessageSayHi):
            if msg['text'] == 'Oi' or msg['text'] == 'oi' or msg['text'] == 'OI':
                message = messages.MessageWhatRegister()

                clear_markup = ReplyKeyboardRemove()
                bot.sendMessage(chat_id, text='Vamos limpar o teclado primeiro...', reply_markup=clear_markup)

                markup = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Peso'), KeyboardButton(text='Refição')],
                    [KeyboardButton(text='Sono'), KeyboardButton(text='Stress')],
                    [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                ])

            else:
                print('nadaaaa')
        elif isinstance(state[chat_id], messages.MessageSorry):
            message = messages.MessageSayHi()

    if message is None:
        message = messages.MessageSorry()

    state[chat_id] = message
    bot.sendMessage(chat_id, message.get_text(), reply_markup=markup)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


with open('tokens.secret') as json_raw:
    secret_json = json.load(json_raw)
    TOKEN = secret_json['ELEVE_BOT_TOKEN']



bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)
