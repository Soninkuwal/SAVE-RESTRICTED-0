# User data storage (use a database for production)
user_data = {}

def initialize_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            "logged_in": False,
            "phone": None,
            "custom_words": [],
            "links": [],
            "thumbnail": None,
            "user_name": None,
            "user_profile_link": None,
        }
    return user_data[user_id]

def clear_user_data(user_id):
    if user_id in user_data:
        del user_data[user_id]

def add_user_link(user_id, link):
    user = initialize_user(user_id)
    user["links"].append(link)

def get_user_info(user_id):
    user = initialize_user(user_id)
    return {
        "user_name": user["user_name"],
        "phone": user["phone"],
        "links": user["links"]
    }

def broadcast_message(bot, text):
    for user_id in user_data.keys():
        bot.send_message(user_id, text)
