import telebot
from telebot.types import Message
from config import BOT_TOKEN
from user_data import initialize_user, clear_user_data
from utils import generate_main_menu, generate_settings_menu

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Command: Start
@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    initialize_user(user_id)
    bot.reply_to(
        message,
        "Welcome to the Sports Bot! Use the menu to navigate features.",
        reply_markup=generate_main_menu(),
    )

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

# Command: Back to Main Menu
@bot.message_handler(func=lambda m: m.text == "🔙 Back to Main Menu")
def back_to_main_menu(message: Message):
    bot.reply_to(message, "Main Menu:", reply_markup=generate_main_menu())

# Command: Set Thumbnail
@bot.message_handler(func=lambda m: m.text == "📷 Set Thumbnail")
def set_thumbnail(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        bot.reply_to(message, "Reply to a photo to set it as your thumbnail.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Command: Get Thumbnail
@bot.message_handler(func=lambda m: m.text == "📷 Get Thumbnail")
def get_thumbnail(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        if user["thumbnail"]:
            bot.send_photo(user_id, user["thumbnail"], caption="Here is your thumbnail.")
        else:
            bot.reply_to(message, "No thumbnail set.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Add Word
@bot.message_handler(func=lambda m: m.text == "➕ Add Word")
def add_word(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        bot.reply_to(message, "Send the word to add.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Delete Word
@bot.message_handler(func=lambda m: m.text == "➖ Delete Word")
def delete_word(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        bot.reply_to(message, "Send the word to delete.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Command: Links Menu
@bot.message_handler(func=lambda m: m.text == "🔗 Links")
def links_menu(message: Message):
    user_id = message.from_user.id
    user = initialize_user(user_id)
    if user["logged_in"]:
        links = user.get("links", [])
        if links:
            bot.reply_to(message, f"First: {links[0]}\nLast: {links[-1]}")
        else:
            bot.reply_to(message, "No links found.")
    else:
        bot.reply_to(message, "You need to log in first.")

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
  
