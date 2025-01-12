    from pyrogram import Client, filters
    from pyrogram.types import Message
    from bot.utils.filters import is_user_authenticated
    from bot.database import Database
    from bot.utils.helpers import setup_logger
    from bot.config import REACTION_EMOJI

    db = Database()
    logger = setup_logger(__name__)

    @Client.on_message(filters.command("broadcast") & is_user_authenticated)
    async def send_broadcast_message(client, message):
        if len(message.text.split()) > 1:
            all_user = db.get_all_users()
            message_text = message.text.split(None, 1)[1]
            for user in all_user:
                try:
                    await client.send_message(user['user_id'], message_text)
                except Exception as e:
                    logger.error(f"Error to broadcast message to user:{user['user_id']}", exc_info=True)
            await message.reply('Broadcast message sent')
            await message.react(REACTION_EMOJI)
            logger.info(f"Send Broadcast Message")
        else:
            return await message.reply('Send text with broadcast command')
        await message.react(REACTION_EMOJI)
