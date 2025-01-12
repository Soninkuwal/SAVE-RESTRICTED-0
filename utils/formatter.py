from database import db

async def format_message(message, user_id):
    user = db.get_user_by_telegram_id(user_id)
    if user:
       replace_words = db.get_replace_words_by_user(user[0])
       delete_words = db.get_delete_words_by_user(user[0])
       for old_word, new_word in replace_words:
           message = message.replace(old_word, new_word)
       for word in delete_words:
           message = message.replace(word[0], "")
    return message
