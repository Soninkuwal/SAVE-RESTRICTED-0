from telebot import types

# Generate the main menu
def generate_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📜 Settings", "🔗 Links", "🔓 Login", "🚪 Logout")
    return keyboard

# Generate the settings menu
def generate_settings_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📷 Set Thumbnail", "📷 Get Thumbnail")
    keyboard.add("➕ Add Word", "➖ Delete Word")
    keyboard.add("🔙 Back to Main Menu")
    return keyboard

# Generate links menu
def generate_links_menu(links):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if links:
        keyboard.add(f"First Link: {links[0]}", f"Last Link: {links[-1]}")
    return keyboard

# Generate user info menu
def generate_user_info_menu(user):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(f"User Name: {user['user_name']}")
    keyboard.add(f"Phone: {user['phone']}")
    return keyboard

# Generate broadcast message button
def generate_broadcast_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📡 Broadcast Message")
    return keyboard
