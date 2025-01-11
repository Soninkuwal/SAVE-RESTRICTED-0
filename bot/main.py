import telebot
from telebot.types import Message
from config import BOT_TOKEN, PORT, LOG_CHANNEL
from user_data import initialize_user, clear_user_data, add_user_link, get_user_info, broadcast_message
from utils import generate_main_menu, generate_settings_menu, generate_links_menu, generate_user_info_menu, generate_broadcast_button
import logging

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Enable logging
logging.basicConfig(level=logging.INFO)

# Command: Start
@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    initialize_user(user_id)
    bot.reply_to(message, "Welcome to the Sports Bot! Use the menu to navigate features.", reply_markup=generate_main_menu())

# Command: Login
@bot.message_handler(func=lambda m: m.text == "🔓 Login")
def login(message: Message):
    user_id = message.from_user.id
    bot.reply_to(message, "Please send your phone number using the format: /phone <your_number>")

@bot.message_handler(commands=['phone'])
def save_phone_number(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    try:
        phone_number = message.text.split()[1]
        if phone_number.isdigit():
            user["phone"] = phone_number
            user["logged_in"] = True
            bot.reply_to(message, f"Phone number {phone_number} saved. You are now logged in!")
            bot.send_message(LOG_CHANNEL, f"New user logged in: {user['user_name']} | {phone_number}")
        else:
            bot.reply_to(message, "Invalid phone number format. Use: /phone <your_number>")
    except IndexError:
        bot.reply_to(message, "Please provide a phone number. Example: /phone 1234567890")

# Command: Logout
@bot.message_handler(func=lambda m: m.text == "🚪 Logout")
def logout(message: Message):
    user_id = message.from_user.id
    if user_id in user_data:
        clear_user_data(user_id)
        bot.reply_to(message, "You have been logged out successfully.")
    else:
        bot.reply_to(message, "You are not logged in.")

# Command: Settings Menu
@bot.message_handler(func=lambda m: m.text == "📜 Settings")
def settings_menu(message: Message):
    bot.reply_to(message, "Settings Menu:", reply_markup=generate_settings_menu())

# Command: Add custom word
@bot.message_handler(commands=['addword'])
def add_custom_word(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    word = message.text.split(' ', 1)[1]
    user["custom_words"].append(word)
    bot.reply_to(message, f"Custom word '{word}' added.")

# Command: Delete custom word
@bot.message_handler(commands=['deleteword'])
def delete_custom_word(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    word = message.text.split(' ', 1)[1]
    if word in user["custom_words"]:
        user["custom_words"].remove(word)
        bot.reply_to(message, f"Custom word '{word}' deleted.")
    else:
        bot.reply_to(message, f"Custom word '{word}' not found.")

# Command: Links Menu
@bot.message_handler(func=lambda m: m.text == "🔗 Links")
def links_menu(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        links = user.get("links", [])
        if links:
            bot.reply_to(message, f"First: {links[0]}\nLast: {links[-1]}")
            bot.send_message(message.chat.id, "Here are your links:", reply_markup=generate_links_menu(links))
        else:
            bot.reply_to(message, "No links found.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Command: Add User Link
@bot.message_handler(commands=['addlink'])
def add_link(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.reply_to(message, "Please log in first!")
        return
    link = message.text.split(' ', 1)[1]
    add_user_link(user_id, link)
    bot.reply_to(message, f"Link {link} added successfully.")

# Command: Broadcast Message
@bot.message_handler(commands=['broadcast'])
def broadcast(message: Message):
    if message.from_user.id == YOUR_ADMIN_USER_ID:  # Replace with your admin user ID
        text = message.text.split(' ', 1)[1]
        broadcast_message(bot, text)
        bot.reply_to(message, "Broadcast message sent.")

# Command: Get User Info
@bot.message_handler(commands=['userinfo'])
def user_info(message: Message):
    user_id = message.from_user.id
    user = get_user_info(user_id)
    bot.reply_to(message, f"User Info:\nName: {user['user_name']}\nPhone: {user['phone']}\nLinks: {', '.join(user['links'])}")

# Start the bot
if __name__ == "__main__":
    bot.infinity_polling()
