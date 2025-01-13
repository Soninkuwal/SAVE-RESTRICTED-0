
    from pyrogram import Client, filters
    from pyrogram.types import Message, CallbackQuery
    from bot.keyboards.inline import settings_keyboard, thumbnail_keyboard
    from bot.utils.filters import is_user_authenticated, only_admin
    from bot.utils.helpers import setup_logger
    from bot.database import Database
    from bot.config import REACTION_EMOJI, ADMIN_IDS, LOG_CHANNEL
    import os
    import os
    from dotenv import load_dotenv

    load_dotenv()

    logger = setup_logger(__name__)
    db = Database()

    @Client.on_message(filters.command("settings") & is_user_authenticated)
    @only_admin
    async def settings_menu(client: Client, message: Message):
        await message.reply_text("Settings Menu:", reply_markup=settings_keyboard())
        await message.react(REACTION_EMOJI)

    @Client.on_callback_query(filters.regex("^(upload_thumbnail|replace_words|delete_words|batch_import|cancel_batch|broadcast|delete_thumbnail|add_admin|add_log_channel)$"))
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
        elif action == "add_admin":
            await callback_query.message.reply("Please send the user ID of the new admin.")
        elif action == "add_log_channel":
             await callback_query.message.reply("Please send the log channel ID.")
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


    @Client.on_message(filters.text & is_user_authenticated)
    @only_admin
    async def handle_add_admin_log_channel(client: Client, message: Message):
       if message.reply_to_message:
          if message.reply_to_message.text == "Please send the user ID of the new admin.":
               try:
                  new_admin_id = int(message.text)
                  if new_admin_id not in ADMIN_IDS:
                     ADMIN_IDS.append(new_admin_id)
                     os.environ['ADMIN_IDS'] = ','.join(map(str, ADMIN_IDS))

                     # Update .env file
                     with open(".env", "r") as f:
                      lines = f.readlines()
                     with open(".env", "w") as f:
                         for line in lines:
                             if line.startswith("ADMIN_IDS="):
                                 f.write(f"ADMIN_IDS={os.environ['ADMIN_IDS']}\n")
                             else:
                                 f.write(line)

                     await message.reply(f"Admin ID {new_admin_id} added successfully.")
                  else:
                     await message.reply("This user is already an admin.")
               except ValueError:
                   await message.reply("Invalid User ID. Please send a valid numeric User ID.")

               await message.react(REACTION_EMOJI)
          elif message.reply_to_message.text == "Please send the log channel ID.":
              try:
                    new_log_channel = int(message.text)
                    os.environ['LOG_CHANNEL'] = str(new_log_channel)
                    # Update .env file
                    with open(".env", "r") as f:
                       lines = f.readlines()
                    with open(".env", "w") as f:
                        for line in lines:
                            if line.startswith("LOG_CHANNEL="):
                                f.write(f"LOG_CHANNEL={os.environ['LOG_CHANNEL']}\n")
                            else:
                                f.write(line)
                    global LOG_CHANNEL
                    LOG_CHANNEL= new_log_channel # Update the local variable
                    await message.reply(f"Log Channel ID {new_log_channel} added successfully.")
              except ValueError:
                  await message.reply("Invalid Log Channel ID. Please send a valid numeric Log Channel ID.")
              await message.react(REACTION_EMOJI)
    
