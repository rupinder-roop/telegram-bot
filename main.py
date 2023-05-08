# 6211782264:AAGuclau-NtBWvUSAnoutKekbVqL-VoJUD4

import telebot
import requests
import sys
from telebot import types

chat_id = sys.argv[1]
filename = sys.argv[2]
total = sys.argv[3]
int(total)
print(total)

TOKEN= "6211782264:AAGuclau-NtBWvUSAnoutKekbVqL-VoJUD4"
method="sendMessage"
myuserid="1253812256"
# bot = telebot.TeleBot("6211782264:AAGuclau-NtBWvUSAnoutKekbVqL-VoJUD4")
username = "1442594780"

# create a bot instance
bot = telebot.TeleBot(TOKEN)

def send_order_options(chat_id):
    markup = types.InlineKeyboardMarkup()
    accept_button = types.InlineKeyboardButton("Accept", callback_data="accept")
    decline_button = types.InlineKeyboardButton("Decline", callback_data="decline")
    markup.add(accept_button, decline_button)

    bot.send_message(chat_id, f"Please click the link below to pay ₹{total}:",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data == "accept":
        accept_order()
        bot.answer_callback_query(call.id, "You accepted the order.")

    elif call.data == "decline":
        decline_order()
        bot.answer_callback_query(call.id, "You declined the order.")


def accept_order():
    bot.send_message(chat_id, "Your Order Has Been Recieved and Accepted.")

def decline_order():
    bot.send_message(chat_id, "We're Sorry Order Has Been Declined. Please let us know if we can help with anything else.")

send_order_options(username)




bot.polling()


# import sys
#
# arg1 = sys.argv[1]
# arg2 = sys.argv[2]
#
# print(arg1, arg2,"arugument pased") # Output: hello world
