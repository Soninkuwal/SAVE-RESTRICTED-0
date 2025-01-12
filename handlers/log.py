    from pyrogram import Client, filters
    from pyrogram.types import Message
    from bot.config import LOG_CHANNEL
    from bot.database import Database
    from bot.utils.helpers import setup_logger

    db = Database()
    logger = setup_logger(__name__)

    @Client.on_message(filters.new_chat_members)
    async def log_new_user(client, message):
        for user in message.new_chat_members:
            user_id = user.id
            user_name = user.username
            first_name = user.first_name
            last_name = user.last_name
            profile_pic = await client.get_chat(user_id)

            db.save_user(user_id, user_name, first_name, last_name)
            logger.info(f"New user: {user_id}, {user_name}, {first_name}, {last_name}")

            try:
                await client.send_photo(
                    chat_id=LOG_CHANNEL,
                    photo=profile_pic.photo.big_file_id,
                    caption=f"New user: {user_id} \nUser Name : {user_name} \nFirst Name: {first_name} \nLast Name: {last_name}",
                )
            except Exception as e:
                logger.error(f"Error log new user {user_id} on log channel", exc_info=True)

    @Client.on_message(filters.private & filters.command("start"))
    async def log_private_user(client, message):
        user_id = message.from_user.id
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        profile_pic = await client.get_chat(user_id)

        db.save_user(user_id, user_name, first_name, last_name)
        logger.info(f"New user: {user_id}, {user_name}, {first_name}, {last_name}")
        try:
            await client.send_photo(
                chat_id=LOG_CHANNEL,
                photo=profile_pic.photo.big_file_id,
                caption=f"New user: {user_id} \nUser Name : {user_name} \nFirst Name: {first_name} \nLast Name: {last_name}",
            )
        except Exception as e:
            logger.error(f"Error log new user {user_id} on log channel", exc_info=True)
