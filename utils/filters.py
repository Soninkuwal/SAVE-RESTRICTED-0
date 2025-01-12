    from pyrogram import filters
    from bot.database import Database

    db = Database()

    def is_user_authenticated(func):
        async def wrapper(client, message):
            user_id = message.from_user.id
            status = db.get_user_status(user_id)
            if status == "authenticated":
                return await func(client, message)
            else:
                await message.reply("Please /login first.")
        return wrapper

    def only_admin(func):
        async def wrapper(client, message):
            from bot.utils.helpers import is_admin
            if await is_admin(client, message.from_user.id):
                return await func(client, message)
            else:
                await message.reply('You are not an admin')
        return wrapper

    def only_private_chat(func):
        async def wrapper(client, message):
            if message.chat.type == "private":
                return await func(client, message)
            else:
                return await message.reply("This command only work in private chat")
        return wrapper
