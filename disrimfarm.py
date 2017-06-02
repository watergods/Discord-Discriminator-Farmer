import shutil
import os
import time
import asyncio

try:
    shutil.copyfile("config.ini", "temp.py")
    from temp import *
    os.remove("temp.py")
except:
    raise Exception("[ERROR] Config load error. Probably missing, broken or in a directory with no write permissions.")

if discordtoken == "" and discordpass == "":
    raise Exception("[ERROR] Config not edited.")

def install(package):
    pip.main(['install', package])

import logging
try:
    import discord
except:
    install("discord.py")

print("[NOTE] Signing into Discord. This may take a while.")
logging.basicConfig(level=logging.ERROR)
client = discord.Client()

@client.event
async def on_ready():
    OriginalName = client.user.name
    print("\n------------------")
    print('Logged in as ' + OriginalName)
    print('ID: ' + client.user.id)
    print("------------------\n")
    MemberCount = 0
    ServerCount = 0
    UserList = []
    for server in client.servers:
        ServerCount = ServerCount + 1
        print("[SERVER] " + str(server.name))
        for member in server.members:
            MemberCount = MemberCount + 1
            UserList.append(member)
    if ServerCount == 1:
        print("[MEMBERS] There are approximately " + str(MemberCount) + " members in the 1 server you are in!")
    else:
        print("[MEMBERS] There are approximately " + str(MemberCount) + " members in the " + str(ServerCount) +  " servers you are in!")
    if MemberCount < 30000:
        print("[WARNING] There are under 30,000 members in the combined servers you are in. This may cause issues with the discriminator editing process. We recommend joining a few big guilds such as the Discord API server.")
    if MemberCount > 30000 and ServerCount == 1:
        print("[NOTE] You are only in one server, but that server appears to have over 30,000 users. You should be fine, but if you encounter issues, join another big server.")
    print("\n------------------\n")
    while True:
        AlreadyGotDiscrim = False
        for discrim in discrimlist:
            if discrim == client.user.discriminator:
                AlreadyGotDiscrim = True
        if not AlreadyGotDiscrim:
            FoundNickname = False
            DiscrimName = ""
            for user in UserList:
                if FoundNickname == False:
                    if not client.user.name == user.name and client.user.discriminator == user.discriminator:
                        FoundNickname = True
                        DiscrimName = user.name
            if FoundNickname == False:
                print("[ERROR] Farming could not continue because another user could not be found with the same discriminator. Try joining some more big servers.")
            else:
                await client.edit_profile(password=discordpass, username=DiscrimName)
                if ChangeNicknameBack:
                    await client.edit_profile(password=discordpass, username=OriginalName)
                    print("[NOTE] Username changed and then changed back. Your new discriminator should be " + client.user.discriminator + " unless your connection is slow or has a high ping to Discord, however this will not affect the process.")
                else:
                    print("[NOTE] Username changed. Your new discriminator should be " + client.user.discriminator + " unless your connection is slow or has a high ping to Discord, however this will not affect the process.")
        else:
            print("[NOTE] You appear to already have a discriminator you want. Farming has stopped.")
        if ChangeNicknameBack:
            await asyncio.sleep(3600)
        else:
            await asyncio.sleep(1800)

client.run(discordtoken, bot=False)
