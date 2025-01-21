import os
import importlib
import asyncio
# from .globals import global_bot

compile_mode: bool = True # Set to "True" BEFORE compiling. Set to false if not compiling

compile_mode_static_cogs = [
    "commands.fun",
    "commands.pomodoro",
    "commands.mod"
]

async def load_cogs(bot):
    tasks = []
    if not compile_mode:
        for filename in os.listdir("./commands"):
            if filename.endswith(".py") and filename != "__init__.py" and "dummy" not in filename:
                cog_name = filename[:-3]
                module_name = f"commands.{cog_name}"
                tasks.append(load_cog(bot, module_name, cog_name))
    else:
        for cog in compile_mode_static_cogs:
            tasks.append(load_cog(bot, cog, cog.split(".")[-1]))
    
    await asyncio.gather(*tasks)

async def load_cog(bot, module_name, cog_name):
    try:
        module = importlib.import_module(module_name)
        module.setup(bot)
        print(f"Successfully loaded cog: {cog_name}")
    except Exception as e:
        print(f"Failed to load cog {module_name}: {e}")

