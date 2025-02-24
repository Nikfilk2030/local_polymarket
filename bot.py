# import enum
import logging
import os
import threading

import telebot
from dotenv import load_dotenv

import lib.chip_giver as chip_giver

# import time
# from datetime import datetime


# from telebot.types import (InlineKeyboardButton, InlineKeyboardMarkup,
#                            ReplyKeyboardRemove)


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
        # logging.info("Starting birthday ping thread...")
        # birthday_thread = threading.Thread(target=process_birthday_pings, daemon=True)
        # birthday_thread.start()

        # logging.info("Starting log cleaner thread...")
        # log_cleaner_thread = threading.Thread(target=log_cleaner, daemon=True)
        # log_cleaner_thread.start()

        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)

        logging.info("Starting chip giver thread...")
        chip_giver_thread = threading.Thread(
            target=chip_giver.process_free_chip_giver(bot), daemon=True
        )
        chip_giver_thread.start()

    except KeyboardInterrupt:
        logging.info("Shutting down bot gracefully...")

        chip_giver_thread.join(timeout=2)
        # birthday_thread.join(timeout=2)
        # log_cleaner_thread.join(timeout=2)

    except Exception as e:
        logging.critical(f"Bot polling encountered an error: {e}")
        # utils.log_exception(e)
