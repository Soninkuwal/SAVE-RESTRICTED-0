    import logging
    from bot.config import ADMIN_IDS

    def setup_logger(name, log_file='logs/bot.log', level=logging.INFO):
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    async def is_admin(client, user_id):
         return user_id in ADMIN_IDS
