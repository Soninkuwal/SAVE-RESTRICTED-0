    import logging
    from pyrogram import Client
    from bot.config import API_ID, API_HASH, BOT_TOKEN
    from bot.utils.helpers import setup_logger
    from bot.handlers import start, auth, links, settings, broadcast, log, batch

    logger = setup_logger(__name__)

    if __name__ == "__main__":
        bot = Client(
            "sport_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )

        logger.info("Bot Starting...")
        bot.run()
