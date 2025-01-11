from telebot import types

# Generate the main menu keyboard
def generate_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📜 Settings", "🔗 Links")
    keyboard.add("🔓 Login", "🚪 Logout")
    return keyboard

# Generate the settings menu keyboard
def generate_settings_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📷 Set Thumbnail", "📷 Get Thumbnail")
    keyboard.add("➕ Add Word", "➖ Delete Word")
    keyboard.add("🔙 Back to Main Menu")
    return keyboard
  
