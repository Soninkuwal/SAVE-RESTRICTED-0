from telethon import events, Button
from database import db
from utils import formatter
import asyncio

async def broadcast_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
        await event.respond('Please send the message to broadcast', buttons=None)
        await event.client.add_event_handler(broadcast_input_handler, events.NewMessage(from_users=event.sender_id))

async def broadcast_input_handler(event):
    message = event.text
    user = db.get_user_by_telegram_id(event.sender_id)
    if user:
        formatted_message = await formatter.format_message(message, event.sender_id)
        all_users = [user_data[1] for user_data in db.conn.execute("SELECT telegram_id from users").fetchall()]
        for user_id in all_users:
            try:
                await event.client.send_message(user_id, formatted_message)
                await asyncio.sleep(0.1)  # Avoid flooding
            except Exception as e:
                print(f"Error sending to {user_id}: {e}")
        await event.respond("Message broadcasted Successfully", buttons=[
                     [Button.inline('Settings', data='settings')]
            ])
    else:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    event.client.remove_event_handler(broadcast_input_handler)
