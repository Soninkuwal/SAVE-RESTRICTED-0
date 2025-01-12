    from pyrogram import Client, filters
    from pyrogram.types import Message, CallbackQuery
    from bot.keyboards.inline import settings_keyboard, thumbnail_keyboard
    from bot.utils.filters import is_user_authenticated, only_admin
    from bot.utils.helpers import setup_logger
    from bot.database import Database
    from bot.config import REACTION_EMOJI
    import os

    logger = setup_logger(__name__)
    db = Database()

    @Client.on_message(filters.command("settings") & is_user_authenticated)
    @only_admin
    async def settings_menu(client: Client, message: Message):
        await message.reply_text("Settings Menu:", reply_markup=settings_keyboard())
        await message.react(REACTION_EMOJI)

    @Client.on_callback_query(filters.regex("^(upload_thumbnail|replace_words|delete_words|batch_import|cancel_batch|broadcast|delete_thumbnail)$"))
    @is_user_authenticated
    async def settings_callback(client: Client, callback_query: CallbackQuery):
        action = callback_query.data
        user_id = callback_query.from_user.id

        if action == "upload_thumbnail":
             await callback_query.message.reply("Please upload a thumbnail image.")
        elif action == "replace_words":
             await callback_query.message.reply("Please send the words to replace.")
        elif action == "delete_words":
            await callback_query.message.reply("Please send the words to delete.")
        elif action == "batch_import":
            await callback_query.message.reply("Please send the file with links (txt file)")
        elif action == "cancel_batch":
             await callback_query.message.reply("Batch import cancelled")
        elif action == "broadcast":
             await callback_query.message.reply("Send broadcast message")
        elif action == "delete_thumbnail":
             user_settings = db.get_user_settings(user_id)
             if user_settings and 'thumbnail' in user_settings:
                user_settings['thumbnail'] = None
                db.update_user_settings(user_id, user_settings)
                await callback_query.message.reply("Thumbnail Removed successfully")
             else:
                 await callback_query.message.reply("You dont have any Thumbnail to delete!")
        await callback_query.message.react(REACTION_EMOJI)
        await callback_query.answer()


    @Client.on_message(filters.photo & is_user_authenticated)
    @only_admin
    async def handle_thumbnail(client: Client, message: Message):
         user_id = message.from_user.id
         user_settings = db.get_user_settings(user_id) or {}
         user_settings['thumbnail'] = message.photo.file_id
         db.update_user_settings(user_id,user_settings)
         await message.reply("Thumbnail Added Successfully!",reply_markup=thumbnail_keyboard())
         await message.react(REACTION_EMOJI)
