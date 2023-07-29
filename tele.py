import requests
import logging

# Initialize logger
logging.basicConfig(filename='tele_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def telegram_send_message(message):
    try:
        bot_token = "***********************************************"
        bot_chatID = "*************"
        send_text = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatID + "&parse_mode=Markdown&text=" + message
        response = requests.get(send_text)
        response_json = response.json()
        if response_json.get('ok'):
            logger.info("Telegram message sent successfully.")
        else:
            logger.error("Failed to send Telegram message.")
            logger.error(response_json)
            raise ValueError("Failed to send Telegram message. Please check the log for more details.")

    except Exception as e:
        logger.error("An error occurred while sending Telegram message:", exc_info=True)
        raise ValueError("Failed to send Telegram message. Please check the log for more details.")
    
    return response_json
