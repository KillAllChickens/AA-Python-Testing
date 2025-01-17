import twitchio
# from utils.config import GlobalConfig #Config
from utils.bot import Bot
from utils.api.api import start_api
import webbrowser
import threading
import atexit
import os
import importlib
import time
# import websockets
from utils.websocket import WebSocketServer
import asyncio
import aiohttp
from utils.globals import global_bot
from utils.shared import glob_conf as config

#*************
## Variables
#*************

# config = GlobalConfig()
client_id = None
client_secret = None
access_token = None
refresh_token = None
api_thread = None  # We'll handle this with asyncio later
bot = global_bot.get_var()
websocket_client = None
# print("websocket_client after init:", websocket_client)


#*************
## Functions
#*************

# async def refresh_twitch_token():
#     url = "https://id.twitch.tv/oauth2/token"
#     params = {
#         "grant_type": "refresh_token",
#         "refresh_token": refresh_token,
#         "client_id": client_id,
#         "client_secret": client_secret
#     }
    
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, params=params) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 # return data.get("access_token"), data.get("refresh_token")
#                 config.set_val("access_token", data.get("access_token"))
#                 config.set_val("refresh_token", data.get("refresh_token"))
            
#             else:
#                 error_data = await response.text()
#                 raise Exception(f"Failed to refresh token: {response.status} - {error_data}")

# def load_config() -> None:
#     global config, client_id, client_secret, access_token, refresh_token
#     client_id = config.client_id
#     client_secret = config.client_secret
#     access_token = config.access_token
#     refresh_token = config.refresh_token

# def load_cogs(bot):
#     for filename in os.listdir("./commands"):
#         if filename.endswith(".py") and filename != "__init__.py":
#             cog_name = filename[:-3]
#             module_name = f"commands.{cog_name}"
#             try:
#                 module = importlib.import_module(module_name)
#                 module.setup(bot)
#                 print(f"Successfully loaded cog: {cog_name}")
#             except Exception as e:
#                 print(f"Failed to load cog {module_name}: {e}")

# def load_dummy_cog(bot):
#     try:
#         module = importlib.import_module("commands.dummy")
#         module.setup(bot)
#         print(bot)
#         print(f"Successfully loaded dummy cog")
#     except Exception as e:
#         print(f"Failed to load dummy cog: {e}")


async def start_bot():
    if not bot:
        print("Bot initialization failed, bot is None")
    # load_dummy_cog(bot)
    # await bot.start()

def start_webui():
    print("Starting Web UI!")
    global api_thread
    if not api_thread:
        api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()
    # await start_api()

def end_webui():
    print("Stopping Web UI...")
    if api_thread:
        api_thread.join(timeout=5)

async def token_invalid():
    print("Access token expired or invalid, Authenticating...")
    webbrowser.open("http://localhost:53847")
    await wait_for_token()

async def wait_for_token():
    while not access_token:
        await asyncio.sleep(1)
        load_config()

async def initialize_websocket():
    # print("starting!")
    global websocket_client
    websocket_client = WebSocketServer()
    # await websocket_client.start_server()
    asyncio.create_task(websocket_client.start_server())
    await websocket_client.ready_event.wait()
    print("Websocket running...")
    
# async def initialize_bot():
#     global bot
#     try:
#         if bot is None:
#             bot = Bot()
#             global_bot = bot
#             print("Bot initialized successfully.")
#     except ValueError as e:
#         print(f"Bot initialization failed: {e}")
#         await refresh_twitch_token()
#         load_config()
#         await initialize_bot()

async def initialize_bot():
    global bot, access_token
    # if access_token is None or not access_token.strip():
    #     print("Cannot initialize bot: Access token is missing.")
    #     # await refresh_twitch_token()
    #     load_config()  # Reload updated token

    try:
        if bot is None:
            bot = Bot()
            if global_bot.get_var() is None:
                global_bot.set_var(bot)
            print("Bot initialized successfully.")
    except ValueError as e:
        # ...
        print(f"Bot initialization failed: {e}")
        # Refresh token again and retry, but prevent infinite loop
        # await refresh_twitch_token()
        # load_config()
        # if access_token and access_token.strip():  # Only retry if token was refreshed
        #     await initialize_bot()


async def main():

    await initialize_websocket()
    start_webui()
    await initialize_bot()

    
    await asyncio.gather(
        # (),
        # initialize_websocket(),
        run_bot(),
    )


async def run_bot():
    try:
        # if not access_token:
        #     if refresh_token != "":
        #         # await refresh_twitch_token()
        #         load_config()
        #         await initialize_bot()
                
        #     else:
        #         await token_invalid()
        #         load_config()
        #         await initialize_bot()
        # else:
        #     await initialize_bot()
            # ...
        if bot is not None:
            await start_bot()
    except twitchio.AuthenticationError:
        print("token invalid...")
        await token_invalid()
        # load_config()
        # await start_bot()
        await initialize_bot()
        await start_bot()
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise e

if __name__ == "__main__":
    # load_config()

    atexit.register(end_webui)

    # asyncio.run(main())

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(main())
    loop.run_forever()
