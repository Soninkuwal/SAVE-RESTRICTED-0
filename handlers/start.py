    from pyrogram import Client, filters
    from pyrogram.types import Message, InputMediaPhoto
    from bot.database import Database
    from bot.keyboards.inline import join_buttons
    from bot.utils.filters import is_user_authenticated
    from bot.utils.helpers import setup_logger
    from bot.config import REACTION_EMOJI

    db = Database()
    logger = setup_logger(__name__)

    @Client.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        user_id = message.from_user.id
        user_name = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        db.save_user(user_id, user_name, first_name, last_name)
        logger.info(f"New user: {user_id}, {user_name}, {first_name}, {last_name}")

        links = db.get_links_by_type("public")
        user_settings = db.get_user_settings(user_id)
        thumbnail = user_settings.get('thumbnail', None) if user_settings else None

        media = InputMediaPhoto(
            media=thumbnail if thumbnail else "https://placekitten.com/600/400",
            caption="Welcome to the Sports Bot!\nJoin our channels:",
        )

        if links:
            await message.reply_media_group([media])
            await message.reply_text(text="Join Channels", reply_markup=join_buttons(links))
        else:
            await message.reply_text("No Links Found. Start Using /settings to add links")

        await message.react(REACTION_EMOJI)


    @Client.on_message(filters.command("help"))
    @is_user_authenticated
    async def help_command(client: Client, message: Message):
        await message.reply_text(
            """
        Available Commands:
        /start - Start Bot
        /help - Get help
        /settings - Open bot settings
        /logout - Logout bot

        """
        )
        await message.react(REACTION_EMOJI)
