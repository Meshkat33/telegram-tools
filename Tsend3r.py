# import modules
import json
import asyncio

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
    PeerChannel
)
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.tl.types import InputPeerUser
from rich import print as rprint
from rich.console import Console
from Tbanner import Banner, Author
import json
import csv
import random
import time 
import os
import sys

# clean screen
os.system('cls')

# stylize
console = Console()
Banner()
time.sleep(0.2)
Author()

# your info
api_id = 12345678
api_hash = ''
phone = ''
username = ''


# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    time.sleep(0.3)
    console.print("Client Created", style='bold cyan')
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    try:
        time.sleep(0.3)
        user_input_channel = input('Enter Channel URL(https://t.me/Name):')
    except:
        console.print('\nSomething went wrong please try again:(', style='bold red')
    try:
        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel
    except UnboundLocalError:
        console.print('Goodbye:(', style='bold green')
        sys.exit()
    my_channel = await client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limit,
            hash = 0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    all_user_details = []
    for participant in all_participants:
        all_user_details.append(
            {"id": participant.id})
    time.sleep(1)
    console.print('Saving In file...', style='bold white')
    with open("members.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username = user.username
            else:
                username = ''
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ''
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ''
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name])  
    time.sleep(1)    
    console.print('Members scraped successfully.', style='bold green')
 
    time.sleep(0.5)
    console.print('~'*66, style='bold magenta')
    time.sleep(1)
    users = []
    with open('members.csv',encoding='UTF-8') as ff:
        rows = csv.reader(ff,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['user id'] = int(row[1])
            user['access_hash'] = int(row[2])
            users.append(user)

    try:
        time.sleep(1)
        mode = int(input('Enter 1 to send by user ID or Enter 0 to exit: '))
    except:
        console.print('\nAn error accured...', style='bold red')
    # put your messages
    messages = ["Hello @{}, How are you?", "Hi @{}, What's up?"]

    for user in users:
        if mode == 0:
            console.print('Goodbye...', style='bold magenta')
            sys.exit()
        elif mode == 1:
            receiver = InputPeerUser(user['user id'], user['access_hash'])
        else:
            console.print('Invalid Mode.\n   Exiting...', style='bold red')
            sys.exit()
        message = random.choice(messages)
        try:
            time.sleep(1)
            print('Sending Message to: ',user['username'])
            await client.send_message(receiver, message.format(user['username']))
            time.sleep(1)
            console.print('Waiting 30 seconds...', style='bold yellow')
            time.sleep(30)
            
        except PeerFloodError:
            console.print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.", style='bold red')
            await client.disconnect()
            sys.exit()
        except Exception as e:
            print("Error:", e)
            console.print("Trying to continue...", style='bold yellow')
            continue
        except KeyboardInterrupt:
            console.print("------------------  See You Next Time:)  ------------------", style='bold magenta')
            sys.exit()
       
    await client.disconnect()
    time.sleep(1)
    console.print(" Done:),message send to all users... ", style='bold green')

with client:
    client.loop.run_until_complete(main(phone))
