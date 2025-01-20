from twitchio.ext import commands
from utils.commands import configurable_command
from utils.websocket import WebSocketServer
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.websocket_client = WebSocketServer()
    
    # @commands.command(name="test")
    @configurable_command(name="test")
    async def test_command(self, ctx: commands.Context):
        await ctx.reply("Test command is working!")
    
    # @commands.command(name="motivate")
    @configurable_command(name="motivate")
    async def motivational_quote(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.quotable.io/random?tags=motivational") as resp:
                quote_data = await resp.json()
                await ctx.reply(f"\"{quote_data['content']}\"  - {quote_data['author']}")

    @configurable_command(name="lurk")
    async def add_lurker(self, ctx: commands.Context):
        if self.websocket_client.client:
            await self.websocket_client.send_message_with_username("add_lurker", ctx.author.display_name)

    @configurable_command(name="unlurk")
    async def remove_lurker(self, ctx: commands.Context):
        if self.websocket_client.client:
            await self.websocket_client.send_message_with_username("remove_lurker", ctx.author.display_name)
    
def setup(bot):
    bot.add_cog(Fun(bot))

