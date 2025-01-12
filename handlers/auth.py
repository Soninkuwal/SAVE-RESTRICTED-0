from telethon import events, Button
from telethon.sessions import StringSession
from database import db
import asyncio
import re

async def start_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if user:
        await event.respond('Already logged in', buttons=[
                    [Button.inline('Logout', data='logout')]
                ])
    else:
       await event.respond('Welcome Please Login To Use Bot.', buttons=[
                    [Button.inline('Login', data='login')]
                ])

async def login_callback(event):
        await event.respond('Please send me your phone number with country code (e.g., +15551234567)', buttons=None)
        await event.client.add_event_handler(phone_number_handler, events.NewMessage(from_users=event.sender_id))

async def phone_number_handler(event):
    phone_number = event.text
    if not re.match(r'^\+\d{8,15}$', phone_number):
        await event.respond("Please Enter valid Phone Number with country code (e.g., +15551234567)")
        return
    try:
        user = db.get_user_by_phone(phone_number)
        if user:
            await event.respond(f'User {user[2]} Already Logged In Use /logout')
            return

        await event.respond('Please wait, I am logging you in...')
        new_session = StringSession()
        client = event.client
        # send code
        phone_code = await client.send_code_request(phone_number)

        # Add the code input message handler
        await client.add_event_handler(
          lambda x: code_handler(x, event, phone_code, new_session, phone_number),
          events.NewMessage(from_users=event.sender_id)
        )
    except Exception as e:
        await event.respond(f"Login Failed: {e}")

async def code_handler(event, initial_event, phone_code, new_session, phone_number):
   try:
       code = event.text
       client = event.client
       await client.sign_in(phone_number, code, phone_code)
       session_string = new_session.save()
       if db.add_user(initial_event.sender_id, phone_number, session_string):
           await initial_event.respond(f'Login Successfully With number {phone_number}.', buttons=[
                    [Button.inline('Logout', data='logout')]
                ])
       else:
           await initial_event.respond(f'Login failed try Again With Another Account')

       client.remove_event_handler(code_handler)

   except Exception as e:
       await initial_event.respond(f"Login Failed: {e}")

async def logout_handler(event):
    user = db.get_user_by_telegram_id(event.sender_id)
    if not user:
        await event.respond('You are not logged in')
    else:
      db.delete_user_by_telegram_id(event.sender_id)
      await event.respond('Logout Successfully', buttons=[
                    [Button.inline('Login', data='login')]
                ])
