# adding member to group using telethon

from telethon.sync import TelegramClient
from telethon import events
from telethon.events.common import EventCommon 
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from rich.console import Console
from Tbanner import Banner2, Author
import time
import sys
import csv
import traceback

# checking if user added or not 
class UserAdded(EventCommon):
	def __init__(self):
		self.user_added = True

console = Console()

# your info
api_id = 12345678
api_hash = ''
phone = ''
client = TelegramClient(phone, api_id, api_hash)

async def AddMember():
	await client.connect()
	if not await client.is_user_authorized():
	    await client.send_code_request(phone)
	    await client.sign_in(phone, input('Enter the code: '))

	users = []
	with open('members.csv', encoding='UTF-8') as f:
	    rows = csv.reader(f,delimiter=",",lineterminator="\n")
	    next(rows, None)
	    for row in rows:
	        user = {}
	        user['username'] = row[0]
	        user['id'] = int(row[1])
	        user['access_hash'] = int(row[2])
	        user['name'] = row[3]
	        users.append(user)

	chats = []
	last_date = None
	chunk_size = 200
	groups=[]

	result = await client(GetDialogsRequest(
	             offset_date=last_date,
	             offset_id=0,
	             offset_peer=InputPeerEmpty(),
	             limit=chunk_size,
	             hash = 0
	         ))
	chats.extend(result.chats)

	for chat in chats:
	    try:
	        if chat.megagroup == True:
	            groups.append(chat)
	    except:
	        continue

	time.sleep(0.3)
	console.print('[~] Choose a group to add members: \n', style='bold magenta')
	i=0
	for group in groups:
	    print(str(i) + '- ' + group.title)
	    i+=1

	try:
		time.sleep(0.3)
		g_index = input("\n[~] Enter a Number: ")
		target_group=groups[int(g_index)]
		target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)
	except KeyboardInterrupt:
		console.print("\nGoodbye...", style='bold green')
		sys.exit()
	except IndexError:
		console.print("Choose correct number x_x", style='bold red')
		console.print("See you next time...", style="bold green")
		sys.exit()
	except ValueError:
		console.print("type an integer x_x", style='bold red')
		console.print("See you next time...", style="bold green")
		sys.exit()


	time.sleep(0.3)
	mode = int(input("[~] Enter 1 to add by username or 2 to add by ID: "))

	for user in users:
	    try:
	        if mode == 1:
	            if user['username'] == '':
	                continue
	            user_to_add = await client.get_input_entity(user['username'])
	            print("[~] Adding {}".format(user['username']))

	            if UserAdded:
	            	console.print('[~] User Was Added', style='bold green')
	            	continue
	        elif mode == 2:
	            user_to_add = InputPeerUser(user['id'], user['access_hash'])
	            print("[~] Adding {}".format(user['id']))
	            if UserAdded:
	            	console.print('[*] User Was Added', style='bold green')
	            	continue   
	        
	        else:
	            sys.exit("Invalid Mode Selected. Please Try Again.")
	        await client(InviteToChannelRequest(target_group_entity,[user_to_add]))
	        console.print("Waiting 30 Seconds...", style='bold green')
	        time.sleep(30)
	    except PeerFloodError:
	        console.print("[!] Getting Flood Error from telegram. Script is stopping now. Please try again after some time.", style='bold red')
	    except UserPrivacyRestrictedError:
	        console.print("[!] The user's privacy settings do not allow you to do this. Skipping.", style='bold red')
	    except:
	        traceback.print_exc()
	        console.print("[!] Unexpected Error", style='bold red')
	        
	        continue
with client:
	client.loop.run_until_complete(AddMember())
