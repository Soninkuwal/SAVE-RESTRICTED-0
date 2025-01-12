import asyncio
import logging
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from config import API_ID, API_HASH, BOT_TOKEN, DATABASE_URL, LOG_CHANNEL_ID
from handlers import commands, settings, auth, broadcast
from database import Database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Database(DATABASE_URL)

client = TelegramClient(StringSession(), API_ID, API_HASH)

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await auth.start_handler(event)
    # Log new users
    await log_new_user(event)

async def log_new_user(event):
    user = await client.get_entity(event.sender_id)
    user_details = f"New User: {user.first_name} {user.last_name or ''} (@{user.username})\nUser ID: {user.id}\nProfile: {user.stringify()}"
    try:
        await client.send_message(int(LOG_CHANNEL_ID), user_details)
    except Exception as e:
        logging.error(f"Error sending to log channel: {e}")

@client.on(events.CallbackQuery(data='login'))
async def login_callback(event):
    await auth.login_callback(event)

@client.on(events.NewMessage(pattern='/logout'))
async def logout_handler(event):
    await auth.logout_handler(event)

@client.on(events.NewMessage(pattern='/settings'))
async def settings_handler(event):
    await settings.settings_handler(event)

@client.on(events.CallbackQuery(data='thumbnail'))
async def thumbnail_callback(event):
    await settings.thumbnail_callback(event)

@client.on(events.NewMessage(pattern='/addlink'))
async def addlink_handler(event):
    await commands.addlink_handler(event)

@client.on(events.NewMessage(pattern=r'/show_first_last_(\d+)'))
async def show_first_last_link_handler(event):
    try:
       count = int(event.pattern_match.group(1))
       await commands.show_first_last_link_handler(event, count)
    except ValueError:
        await event.respond("Invalid command. Please use /show_first_last_number")

@client.on(events.NewMessage(pattern='/batch_addlink'))
async def batch_addlink_handler(event):
    await commands.batch_addlink_handler(event)

@client.on(events.NewMessage(pattern='/batch_deletelink'))
async def batch_deletelink_handler(event):
    await commands.batch_deletelink_handler(event)

@client.on(events.NewMessage(pattern='/replace_link'))
async def replace_link_handler(event):
     await commands.replace_link_handler(event)

@client.on(events.NewMessage(pattern='/cancel_batch_link'))
async def cancel_batch_link_handler(event):
     await commands.cancel_batch_link_handler(event)

@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast_handler(event):
    await broadcast.broadcast_handler(event)

@client.on(events.CallbackQuery(data='add_replace_word'))
async def add_replace_word_callback(event):
    await settings.add_replace_word_callback(event)

@client.on(events.CallbackQuery(data='add_delete_word'))
async def add_delete_word_callback(event):
    await settings.add_delete_word_callback(event)

async def main():
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
