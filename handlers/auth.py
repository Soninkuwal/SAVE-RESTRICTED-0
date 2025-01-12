    from pyrogram import Client, filters
    from pyrogram.types import Message
    from bot.database import Database
    from bot.utils.helpers import setup_logger
    from bot.utils.filters import only_private_chat
    from bot.config import REACTION_EMOJI

    db = Database()
    logger = setup_logger(__name__)

    @Client.on_message(filters.command("login") & only_private_chat)
    async def login(client: Client, message: Message):
        user_id = message.from_user.id
        if db.get_user_status(user_id) == 'authenticated':
            return await message.reply_text("You are already logged in!")

        sent = await message.reply_text(f"Enter Your Phone Number With Country Code (+XX) :")
        await client.listen(filters.text, timeout=120, chat_id=message.chat.id)
        try:
            phone_number = (await client.listen(filters.text, timeout=120, chat_id=message.chat.id)).text
            if phone_number:
                db.update_user_status(user_id, 'pending')
                res = await client.send_code(phone_number)
                sent_code = await message.reply_text("Enter your code:", reply_to_message_id=sent.id)
                otp = (await client.listen(filters.text, timeout=120, chat_id=message.chat.id)).text
                if otp:
                    await client.sign_in(phone_number, res.phone_code_hash, otp)
                    db.update_user_status(user_id, 'authenticated')
                    await message.reply_text("Login Successful")
                    await message.react(REACTION_EMOJI)
                    return logger.info(f"Login Successful for user: {user_id}")
                else:
                    await message.reply("Time out! Please try again.")
                    await message.react(REACTION_EMOJI)
                    return db.update_user_status(user_id, 'not_authenticated')
            else:
                await message.reply("You have not Provided a valid phone number")
                await message.react(REACTION_EMOJI)
                return db.update_user_status(user_id, 'not_authenticated')
        except Exception as e:
            db.update_user_status(user_id, 'not_authenticated')
            await message.react(REACTION_EMOJI)
            return await message.reply_text(f"Error while login {e}")

    @Client.on_message(filters.command("logout") & only_private_chat)
    async def logout(client: Client, message: Message):
        user_id = message.from_user.id
        if db.get_user_status(user_id) == 'authenticated':
            db.update_user_status(user_id, 'not_authenticated')
            await message.reply_text("Logged out successfully!")
            await message.react(REACTION_EMOJI)
            return
        else:
            await message.reply_text("You are not logged in yet!")
            await message.react(REACTION_EMOJI)
            return
