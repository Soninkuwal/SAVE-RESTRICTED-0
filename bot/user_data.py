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
        }
    return user_data[user_id]

def clear_user_data(user_id):
    if user_id in user_data:
        del user_data[user_id]
