from twitchio.ext import commands
from twitchio.errors import AuthenticationError
from .config import GlobalConfig #Config
import sys
import asyncio
from .api.api import failed_auth
from .shared import glob_conf
from .bot_utils import load_cogs
from .globals import global_bot

# from .globals import global_bot

class Bot(commands.Bot):
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Bot, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # TODO: ↓ Make this load in from global configuration(file location sent from godot) ↓
        print("Bot Class Loaded")
        # self.initial_channels = [ "epicman21221" ] 
        
        # self.prefix = '?'
        self.config = glob_conf # GlobalConfig()
        
        # if not self.config.access_token:
        #     raise ValueError("Access token is missing or invalid!")
        
        # self.access_token = self.config.access_token
        # print(f"Access Token: {self.access_token}")
        
        super().__init__(token="", prefix="", initial_channels=[])

    async def event_ready(self):
        print("-------------------------------")
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await self.join_channels([ self.config.username ])
        self._prefix = self.config.command_prefix
        print(f"self.config.command_prefix says '{self.config.command_prefix}', self._prefix says '{self._prefix}'")
        print(self.commands)

    async def event_command_error(self, ctx: commands.Context, error):
        command = ctx.message.content.split(" ")[0]
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f"Command {command} not found.")
        raise error

    async def process_packet(self, packet_str: str):
        if packet_str.startswith("send_message"):
            await self.send_uninvoked_message(packet_str.split(":", 1)[-1])
        elif packet_str.startswith("end_python"):
            raise SystemExit(int(packet_str.split(":", 1)[-1]))
        elif packet_str.startswith("load_config"):
            # self.config.config_file = packet_str.split(":", 1)[-1]
            print("! LOADING CONFIG !")
            self.config.set_config_file(packet_str.split(":", 1)[-1])
            self.token = self.config.access_token
            self._prefix = self.config.command_prefix

            # Reinitialize bot's internal state
            super().__init__(token=self.token, prefix=self._prefix, initial_channels=[])

            # Reload cogs
            await load_cogs(self)
        elif packet_str.startswith("start_twitch"):
            # print(self.commands)
            asyncio.create_task(self.start_bot())
    
    async def start_bot(self):
        try:
            print(f"{self.token} | '{self._prefix}'")
            await self.start()
        except AuthenticationError:
            await failed_auth(self.config.config)
            self.config.reload_config()
            self.token = self.config.access_token
            self._prefix = self.config.command_prefix
            super().__init__(token=self.token, prefix=self._prefix, initial_channels=[])
            await load_cogs(self)

            await self.start()
            # print(f"Error starting the bot: {e}")

    
    async def send_uninvoked_message(self, message: str):
        # channel = self.get_channel('epicman21221')
        print("sending message")
        channels = self.connected_channels
        for channel in channels:
            await channel.send(message)
