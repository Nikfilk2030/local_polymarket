# import enum
import logging
import os

import telebot
from dotenv import load_dotenv

# import threading
# import time
# from datetime import datetime


# from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
#                            ReplyKeyboardRemove)

# import db
# import utils

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(),
    ],
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logging.critical("TELEGRAM_BOT_TOKEN is not set in the .env file!")
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the .env file!")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_name = (
        message.from_user.first_name or message.from_user.username or "undefined_name"
    )
    bot.reply_to(message, f"Привет, {user_name}!")


if __name__ == "__main__":
    # db.init_db()

    logging.info("Bot is running...")
    try:
        # logging.info("Starting backup ping thread...")
        # backup_thread = threading.Thread(target=process_backup_pings, daemon=True)
        # backup_thread.start()

        # logging.info("Starting birthday ping thread...")
        # birthday_thread = threading.Thread(target=process_birthday_pings, daemon=True)
        # birthday_thread.start()

        # logging.info("Starting log cleaner thread...")
        # log_cleaner_thread = threading.Thread(target=log_cleaner, daemon=True)
        # log_cleaner_thread.start()

        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)

    except KeyboardInterrupt:
        logging.info("Shutting down bot gracefully...")

        # backup_thread.join(timeout=2)
        # birthday_thread.join(timeout=2)
        # log_cleaner_thread.join(timeout=2)

    except Exception as e:
        logging.critical(f"Bot polling encountered an error: {e}")
        # utils.log_exception(e)
