import gtts
a = {
    'ru': 'Russian',
    'en': 'English',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'es': 'Spanish',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'sk': 'Slovak',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'sv': 'Swedish',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'vi': 'Vietnamese'
}
bot = telebot.TeleBot(TOKEN)
Settings = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
Settings.row('Settings')

keyboard1 = telebot.types.InlineKeyboardMarkup()
language = telebot.types.InlineKeyboardButton(
    "Languages", callback_data="Languages")
developer = telebot.types.InlineKeyboardButton(
    "Developer", callback_data="Developer")
keyboard1.add(language, developer)

developer_ex = telebot.types.InlineKeyboardMarkup()
telegram = telebot.types.InlineKeyboardButton(
    text="Telegram", url="https://t.me/Hornet_21")
instagram = telebot.types.InlineKeyboardButton(
    text="Instagram", url="https://instagram.com/solosyre.0")
developer_ex.add(telegram, instagram)

language_ex = telebot.types.InlineKeyboardMarkup(row_width=4)
langs_list = []
for s, n in a.items():
    langs_list.append(n)
for i in range(0, len(a), 4):
    l_button = telebot.types.InlineKeyboardButton(
        text=langs_list[i], callback_data=langs_list[i])
    l_button2 = telebot.types.InlineKeyboardButton(
        text=langs_list[i+1], callback_data=langs_list[i+1])
    l_button3 = telebot.types.InlineKeyboardButton(
        text=langs_list[i+2], callback_data=langs_list[i+2])
    l_button4 = telebot.types.InlineKeyboardButton(
        text=langs_list[i+3], callback_data=langs_list[i+3])
    language_ex.add(l_button, l_button2, l_button3, l_button4)
session = {
    'random': {
        "lang": 'en',
        "passed": True
    }
}


def sender(way, str_, ln1, passd):
    if way:
        for i, n in a.items():
            if str_ == n:
                lang_ = i
                passed = True
                return lang_, passed
    else:
        if passd:
            y_text = str_
            answer = gtts.gTTS(y_text, lang=ln1)
            answer.save("voice.mp3")
            with open("voice.mp3", "rb") as fp:
                f = fp.read()
            return f


@bot.message_handler(commands=["start"])
def starter(message):
    bot.send_message(
        message.chat.id, "Hello its converter bot from text to audio\n Please set the options!", reply_markup=Settings)


@bot.message_handler(content_types="text")
def select_lang(message):
    if not message.text == "Settings":
        if str(message.from_user.username) not in session.keys():
            ses_id = str(message.from_user.username)
            user = {
                'lang': 'en',
                'passed': True
            }
            session[ses_id] = user
        answer = sender(False, message.text, session[str(
            message.from_user.username)]['lang'], session[str(message.from_user.username)]['passed'])
        bot.send_audio(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "Settings:", reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data == "Languages":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Please select the language", reply_markup=language_ex)
    elif call.data == "Developer":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Developer in social networks", reply_markup=developer_ex)
    elif call.data in langs_list:
        ses_id = str(call.from_user.username)
        ln_, passed_ = sender(True, call.data, 'en', True)
        user = {
            'lang': ln_,
            'passed': passed_
        }
        session[ses_id] = user
        bot.send_message(call.message.chat.id, "Please send me your text")


bot.polling()
