from twitchio.ext import commands
from utils.websocket import WebSocketServer
from utils.commands import configurable_command
import asyncio
from typing import Optional

class Pomodoro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.websocket_client = WebSocketServer()

    # @commands.command(name="get_code")
    @configurable_command(name="get_code")
    async def send_code(self, ctx: commands.Context):
        # if not self.websocket_client:
        #     self.websocket_client = WebSocketServer()
        # print(self.websocket_client.client)
        if self.websocket_client.client:
            # print(self.websocket_client)
            
            await self.websocket_client.send_message_with_username("get_code", ctx.author.display_name)
            
            # code = await self.wait_for_response()

            # print(f"code = {code}")

            # if code:
            #     await ctx.reply(f"The code is: {code}")
        else:
            await ctx.reply("No WebSocket client connected!")

    # @commands.command(name="pat")
    @configurable_command(name="pat")
    async def pat_teemo(self, ctx: commands.Context, count: int = 1):
        if count > 3:
            await ctx.reply("Only 3 pats per message! Patting thrice.")
            count = 3
        
        print(f"{ctx.author.name} patted Teemo {count} times!")
        if self.websocket_client.client:
            # print(self.websocket_client.client)
            await self.websocket_client.send_message_with_username("pat_teemo", ctx.author.display_name, str(count))
        else:
            await ctx.reply("No WebSocket client connected")
    
    
    
    # async def wait_for_response(self):
    #     print("Waiting for response...")
    #     return await self.websocket_client.wait_for_response()
    

def setup(bot):
    bot.add_cog(Pomodoro(bot))

