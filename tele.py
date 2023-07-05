import requests

def telegram_send_message(message):
    bot_token = "6201090588:AAFR2ut1z-ii10uHZVFJ89YAjET59I8gIRE"
    bot_chatID = "-1001901512099"
    send_text = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + "&parse_mode=Markdown&text=" + message
    response = requests.get(send_text)
    return response.json()
