from twitchio.ext import commands
from utils.commands import configurable_command
import aiohttp

class Dummy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Dummy(bot))