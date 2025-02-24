import logging
import time

from telebot import TeleBot

import lib.db as db
import lib.user_profile as user_profile
import lib.utils as utils


def last_free_chip_was_given_long_ago(user: user_profile.TUserProfile) -> bool:
    return user.last_free_chip_timestamp + utils.SECONDS_IN_DAY < time.now()


def give_new_day_chips(bot: TeleBot) -> None:
    all_users = []  # TODO: db.get_all_users()
    for user in all_users:
        if not last_free_chip_was_given_long_ago(user):
            continue

        db.update_last_free_chip_timestamp(user.tg_id)
        db.set_chips(user.tg_id, user.balance + utils.FREE_CHIPS_PER_PERIOD)
        bot.send_message(user.chat_id, "🎂")


def process_free_chip_giver(bot: TeleBot) -> None:
    while True:
        minutes = 5
        time.sleep(utils.SECONDS_IN_MINUTE * minutes)
        try:
            give_new_day_chips(bot)
        except Exception as e:
            logging.error(f"Error in free chip giver: {e}")
