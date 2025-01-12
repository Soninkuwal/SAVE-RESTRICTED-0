    from pyrogram import Client, filters
    from pyrogram.types import Message
    from bot.database import Database
    from bot.utils.filters import is_user_authenticated, only_admin
    from bot.utils.helpers import setup_logger
    from bot.config import REACTION_EMOJI

    db = Database()
    logger = setup_logger(__name__)

    @Client.on_message(filters.command("add_link") & is_user_authenticated)
    @only_admin
    async def add_link(client: Client, message: Message):
        if len(message.command) < 3:
            return await message.reply("Please use /add_link <type> <link>")
        link_type, link = message.command[1], message.command[2]

        if not link_type in ['public', 'private', 'topic']:
            return await message.reply('Use only public or private or topic')
        if db.link_exists(link):
            return await message.reply("Link is already added")

        link_id = db.add_link(link_type, link)
        logger.info(f"Added new link: {link_id}, Type:{link_type}, Link: {link}")
        await message.reply(f"Link added successfully! ID: {link_id}")
        await message.react(REACTION_EMOJI)


    @Client.on_message(filters.command("delete_link") & is_user_authenticated)
    @only_admin
    async def delete_link(client: Client, message: Message):
        if len(message.command) < 2:
            return await message.reply("Please use /delete_link <link_id>")
        link_id = message.command[1]

        if db.delete_link(link_id):
            logger.info(f"Link Deleted: {link_id}")
            await message.reply("Link Deleted Successfully")
            await message.react(REACTION_EMOJI)
        else:
            await message.reply("Failed to delete link")
            await message.react(REACTION_EMOJI)
