from twitchio.ext import commands
from utils.commands import configurable_command
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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


def setup(bot):
    bot.add_cog(Fun(bot))

