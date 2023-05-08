

import telebot
import requests
import subprocess
# import request
import stripe
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types

import os
import sys
import time
while True:
    try:
        TOKEN='6148311579:AAFns1m5izqTlnwXWBjkLYVSwXG7QvwBUCs'
        DELIVERIES_DIR = 'deliveries'

        if not os.path.exists(DELIVERIES_DIR):
            os.makedirs(DELIVERIES_DIR)

        # Initialize the bot
        bot = telebot.TeleBot(TOKEN)

        # Define the menu
        menu = {
            "Split Gram Letil (half KG)":60 ,
            "Urad Dal (half KG)":65 ,
            "Kadalal Paruappu(250 gm)": 22,
            "Pepper(100 gm)": 43,
            "Cumin(100gm)": 26,
            "Mustard(100 gm)": 9,
            "Coriander(200 gm)":24,
            "Turmeric Powder(100 gm)":13,
            "Garlic(250 gm)":50,
            "Gold Winner Sunflowe Oil(200gm)":25,
            "Chilly Powder(100 gm)":25,
            "Milk":30
        }

        # Define the inventory
        inventory = {
            "Split Gram Letil (half KG)":20 ,
            "Urad Dal (half KG)":30,
            "Kadalal Paruappu(250 gm)": 25,
            "Pepper(100 gm)": 50,
            "Cumin(100gm)": 30,
            "Mustard(100 gm)": 60,
            "Coriander(200 gm)":45,
            "Turmeric Powder(100 gm)":35,
            "Garlic(250 gm)":50,
            "Gold Winner Sunflowe Oil(200gm)":100,
            "Chilly Powder(100 gm)":35,
            "Milk":150
        }

        # Define the cart
        cart = {}


        # Set your API key

        stripe.api_key = "sk_test_51N4mnOSI0XD3l8PpPYqODQ92pijrr3SAoktruhpD8cX1bxGeX9fHzLA36FK2Gzm4FSgQCk1mV7gDGyLC3zWTKSWV004GuiZaO2"
        webhook_secret='whsec_8d4e611de374409718e91ad19eff2c6fa8bee946d20cc81208a1837dea0a7657'
        # Define the start message handler
        @bot.message_handler(commands=["start"])
        def send_welcome(message):
            # Create the start message
            start_message = "Welcome to our Store! Here's Item Listed:\n\n"

            # Add the menu items to the message
            for item, price in menu.items():
                start_message += "{} - ₹{:.2f}\n".format(item, price)

            # Send the message and display the menu as buttons
            bot.send_message(message.chat.id, start_message, reply_markup=create_menu_keyboard())


        # Define the function to create the menu keyboard
        def create_menu_keyboard():
            # Create the keyboard
            keyboard = types.InlineKeyboardMarkup()

            # Add the menu items as buttons
            for item in menu:
                button = types.InlineKeyboardButton(item, callback_data=item)
                keyboard.add(button)

            # Add the "View Cart" and "Checkout" buttons
            cart_button = types.InlineKeyboardButton("View Cart", callback_data="cart")
            checkout_button = types.InlineKeyboardButton("Checkout", callback_data="checkout")
            keyboard.row(cart_button, checkout_button)

            # Return the keyboard
            return keyboard


        # Define the callback query handler for menu item buttons
        @bot.callback_query_handler(func=lambda call: call.data in menu.keys())
        def process_menu_callback(call):
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            item = call.data

            # Add the item to the cart or increase the quantity
            if item in cart:
                cart[item] += 1
            else:
                cart[item] = 1

            # Update the message with the current cart contents
            cart_text = "Your cart:\n"
            for item, quantity in cart.items():
                cart_text += f"{item}: {quantity}\n"
            bot.edit_message_text(cart_text, chat_id, message_id, reply_markup=create_menu_keyboard())


        # Define the callback query handler for the "View Cart" button
        @bot.callback_query_handler(func=lambda call: call.data == "cart")
        def process_cart_callback(call):
            # Create the cart message
            cart_message = "Your cart:\n\n"
            for item, quantity in cart.items():
                cart_message += "{} x {} = ₹{}\n".format(item, quantity,menu[item]*quantity)
            total = 0
            for item, quantity in cart.items():
                total += menu[item] * quantity
            cart_message += "\nTotal: ₹{:.2f}".format(total)

            # Send the cart message and display the menu as buttons
            bot.send_message(call.message.chat.id, cart_message, reply_markup=create_menu_keyboard())


        # Handler for the "Pay" button
        @bot.callback_query_handler(func=lambda call: call.data == "checkout")
        def process_pay_callback(call):
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            # Calculate the total amount and reset the cart
            total = 0
            for item, quantity in cart.items():
                total += menu[item] * quantity

            keyboard = types.InlineKeyboardMarkup()
            pay_button = types.InlineKeyboardButton("Pay Now", callback_data="pay")
            keyboard.row(pay_button)

            bot.send_message(chat_id, f"Please click the link below to pay ₹{total}:", reply_markup=keyboard)



        @bot.callback_query_handler(func=lambda call: call.data == "pay")
        def process_pay_callback(call):
            chat_id=call.message.chat.id

            total = 0
            for item, quantity in cart.items():
                total += menu[item] * quantity

            create_payment_intent()
            msg = bot.send_message(chat_id, "Please enter your delivery information:")
            bot.register_next_step_handler(msg, process_delivery_info, chat_id, total)

        # Create a payment intent
        def create_payment_intent():
            total = 0
            for item, quantity in cart.items():
                total += menu[item] * quantity
            intent = stripe.PaymentIntent.create(
                amount=total*100,
                currency='inr',
            )

            return intent

        # Get the client secret of a payment intent
        def get_client_secret(payment_intent_id):
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return intent.client_secret


        def process_delivery_info(message, chat_id, total):
            # Store delivery information in a file
            address = message.text
            if not os.path.exists(DELIVERIES_DIR):
                os.makedirs(DELIVERIES_DIR)
            order_number = len(os.listdir("deliveries")) + 1
            filename = f"order_{order_number}.txt"
            with open(os.path.join(DELIVERIES_DIR,filename), "w") as file:
                file.write(f"Order Number: {order_number}\n")
                file.write("Items:\n")

                for item, quantity in cart.items():
                    file.write(f"{item} * {quantity} = {menu[item]*quantity}\n")
                file.write(f"Address: {address}\n")
                file.write(f"Total: {total}\n")
            cart.clear()



            bot.send_message(chat_id, "Thank you for your order!")
            subprocess.call(["python", "main.py",str(chat_id),str(filename),str(total)])



        def process_order(chat_id,message_id):
            # Check if delivery information is available
            filename = f"{chat_id}_{message_id}.txt"
            filepath = os.path.join(DELIVERIES_DIR, filename)
            if not os.path.exists(filepath):
                bot.send_message(chat_id, "Sorry, we don't have your delivery information. Please place an order again.")
                return

            # Process the order
            with open(filepath, "r") as f:
                delivery_info = f.read()
                bot.send_message(chat_id, f"Your order has been processed. Delivery Information: {delivery_info}")

                # Remove the delivery file
                os.remove(filepath)



        def send_order_to_shopkeeper(chat_id, order_message):
            # Replace with the actual shopkeeper chat ID
            shopkeeper_chat_id = 123456789
            # Send the order message to the shopkeeper
            bot.send_message(chat_id=shopkeeper_chat_id, text=order_message)
            # Wait for the shopkeeper's response
            bot.send_message(chat_id=chat_id, text="Waiting for the shopkeeper's response...")
            @bot.message_handler(func=lambda message: message.chat.id == shopkeeper_chat_id)
            def process_shopkeeper_response(message):
                if message.text.lower() == "accept":
                    bot.send_message(chat_id=chat_id, text="Your order has been accepted. Please proceed with the payment.")
                elif message.text.lower() == "decline":
                    bot.send_message(chat_id=chat_id, text="Sorry, your order has been declined. Please try again later.")
                else:
                    bot.send_message(chat_id=chat_id, text="Invalid response. Please try again later.")

        # send_order_to_shopkeeper('123456789',"Order")

        print("starting before");
        bot.polling()
        print("starting")
    except Exception as e:
        # print(f"An error occurred: {e}")
        print("Restarting the program...")
        time.sleep(1)
        # restart the program
        python = sys.executable
        os.execl(python, python, *sys.argv)

