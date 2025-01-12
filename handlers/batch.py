    from pyrogram import Client, filters
    from pyrogram.types import Message, CallbackQuery
    from bot.utils.filters import is_user_authenticated, only_admin
    from bot.database import Database
    from bot.utils.helpers import setup_logger
    from bot.keyboards.inline import cancel_keyboard
    from bot.config import REACTION_EMOJI

    db = Database()
    logger = setup_logger(__name__)
    BATCH_LINKS = []
    import_process_active = False

    @Client.on_message(filters.document & is_user_authenticated)
    @only_admin
    async def batch_link_import(client, message):
        if import_process_active:
            return await message.reply("Import process is currently on going...")
        await message.react(REACTION_EMOJI)
        file_path = await client.download_media(message.document)
        try:
            with open(file_path, 'r') as f:
                BATCH_LINKS = f.read().splitlines()
                global import_process_active
                import_process_active = True
                await message.reply(f"Start Batch Import. Total Links Found: {len(BATCH_LINKS)}", reply_markup=cancel_keyboard())
                for link in BATCH_LINKS:
                    link_type = "public"
                    if not db.link_exists(link):
                        db.add_link(link_type, link)
                    else:
                        logger.info(f'Link already exist in database')
                await message.reply("Batch import Completed.")
                import_process_active = False
        except Exception as e:
            await message.reply(f"Error while importing file : {e}")
            import_process_active = False

        import os
        os.remove(file_path)

    @Client.on_callback_query(filters.regex("^cancel$"))
    @is_user_authenticated
    async def cancel_import(client: Client, callback_query: CallbackQuery):
        global import_process_active
        import_process_active = False
        await callback_query.message.reply("Batch import cancelled")
        await callback_query.message.react(REACTION_EMOJI)
        await callback_query.answer()
