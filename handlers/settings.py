from telethon import events, Button
from database import db
import asyncio
from config import BOT_TOKEN

async def settings_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    else:
        await event.respond("Settings", buttons=[
            [Button.inline('Custom Thumbnail', data='thumbnail')],
            [Button.inline('Add Replace Word', data='add_replace_word')],
            [Button.inline('Add Delete Word', data='add_delete_word')]
            ])

async def thumbnail_callback(event):
    await event.respond('Please send me the URL of the custom thumbnail', buttons=None)
    await event.client.add_event_handler(thumbnail_handler, events.NewMessage(from_users=event.sender_id))

async def thumbnail_handler(event):
    thumbnail_url = event.text
    user = db.get_user_by_telegram_id(event.sender_id)
    if user:
         db.set_user_thumbnail(user[1], thumbnail_url)
         await event.respond("Thumbnail set Successfully", buttons=[
                     [Button.inline('Settings', data='settings')]
             ])
    else:
         await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                ])
    event.client.remove_event_handler(thumbnail_handler)

async def add_replace_word_callback(event):
    await event.respond('Please send the old word followed by the new word, separated by a comma\n(Example: old, new)', buttons=None)
    await event.client.add_event_handler(add_replace_word_handler, events.NewMessage(from_users=event.sender_id))

async def add_replace_word_handler(event):
    text = event.text
    parts = text.split(',')
    if len(parts) == 2:
         old_word, new_word = parts
         user = db.get_user_by_telegram_id(event.sender_id)
         if user:
              db.add_replace_word(user[0], old_word.strip(), new_word.strip())
              await event.respond(f"Replace word Successfully added old word {old_word.strip()} with new word {new_word.strip()}", buttons=[
                     [Button.inline('Settings', data='settings')]
                 ])
         else:
             await event.respond("Please Login First To Set Settings /start", buttons=[
                    [Button.inline('Login', data='login')]
                 ])
    else:
        await event.respond("Invalid input format! Please send `old, new`")
    event.client.remove_event_handler(add_replace_word_handler)

async def add_delete_word_callback(event):
    await event.respond('Please send the word you want to delete.', buttons=None)
    await event.client.add_event_handler(add_delete_word_handler, events.NewMessage(from_users=event.sender_id))

async def add_delete_word_handler(event):
    word = event.text
    user = db.get_user_by_telegram_id(event.sender_id)
    if user:
        db.add_delete_word(user[0], word.strip())
        await event.respond(f"Delete word '{word.strip()}' added successfully", buttons=[
                [Button.inline('Settings', data='settings')]
            ])
    else:
         await event.respond("Please Login First To Set Settings /start", buttons=[
                [Button.inline('Login', data='login')]
            ])
    event.client.remove_event_handler(add_delete_word_handler)
