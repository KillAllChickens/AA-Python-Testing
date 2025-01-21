from twitchio.ext import commands
from utils.commands import configurable_command
from utils.websocket import WebSocketServer
import aiohttp
from typing import Optional

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.websocket_client = WebSocketServer()
    
    @configurable_command(name="removefrom", always_on=True)
    async def delete_all_messages_from(self, ctx: commands.Context, user: str):
        if (not ctx.author.is_mod) and (not ctx.author.is_broadcaster):
            await ctx.reply("You must be a moderator in order to use this command.")

        if self.websocket_client.client:
            await self.websocket_client.send_message_with_username("remove_from", ctx.author.display_name, user)



def setup(bot):
    bot.add_cog(Mod(bot))


