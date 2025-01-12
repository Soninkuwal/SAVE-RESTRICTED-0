    from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    def join_buttons(links):
        keyboard = []
        for link in links:
            keyboard.append([InlineKeyboardButton(text="Join Channel", url=link['link'])])
        return InlineKeyboardMarkup(keyboard)

    def settings_keyboard():
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Upload Thumbnail", callback_data="upload_thumbnail")],
                [InlineKeyboardButton("Replace Words", callback_data="replace_words")],
                [InlineKeyboardButton("Delete Words", callback_data="delete_words")],
                [InlineKeyboardButton("Batch Import", callback_data="batch_import")],
                [InlineKeyboardButton("Cancel Batch", callback_data="cancel_batch")],
                [InlineKeyboardButton("Broadcast", callback_data="broadcast")],
            ]
        )

    def cancel_keyboard():
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="cancel")],
            ]
        )
    
    def thumbnail_keyboard():
        return InlineKeyboardMarkup(
           [
                [InlineKeyboardButton("Delete Thumbnail", callback_data="delete_thumbnail")],
           ]
              )
