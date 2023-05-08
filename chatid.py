#
# # BOT_TOKEN = '6211782264:AAGuclau-NtBWvUSAnoutKekbVqL-VoJUD4'
#
BOT_TOKEN='6148311579:AAFns1m5izqTlnwXWBjkLYVSwXG7QvwBUCs'
import requests
import sys
import os

idchat = sys.argv[1]
filename = sys.argv[2]
total=sys.argv[3]
# filename=f"order_{order_number}.txt"
directory = "deliveries"
def process_order():
    # Check if delivery information is available
    DELIVERIES_DIR="deliveries"
    # filename = f"{chat_id}_{message_id}.txt"
    filepath = os.path.join(DELIVERIES_DIR, filename)
    if os.path.exists(filepath):
        print("yes")

    # Process the order
    with open(filepath, "r") as f:
        delivery_info = f.read()

process_order()
# TARGET_BOT_ID = '6148311579:AAFns1m5izqTlnwXWBjkLYVSwXG7QvwBUCs'
MESSAGE = 'Hello from one bot to another!'
TARGET_BOT_ID="1253812256"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
params = {
    "chat_id": idchat,
    "text": "Order Confirmed"
}

# Send the message using the requests library
response = requests.post(url, data=params)
#



# # Check if the message was sent successfully
# if response.status_code == 200:
#     print("Message sent successfully!")
# else:
#     print(f"Error sending message: {response.status_code} - {response.text}")

# 1 15 17
# 16 30 18
# 31 45 19
# 46 60 20

# import subprocess
#
# # Set the arguments to be passed to the other file
# arg1 = "hello"
# arg2 = "world"
#
# # Run the other Python file and pass the arguments
# subprocess.call(["python", "main.py", arg1, arg2])


