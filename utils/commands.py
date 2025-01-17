from twitchio.ext.commands import command
from typing import Optional, Callable
# from .config import GlobalConfig
from .shared import glob_conf as config

# config = GlobalConfig()
enabled_commands = config.get_enabled_commands()

print(enabled_commands)
# print(config.commands)

def configurable_command(*, name: Optional[str] = None) -> Callable: 
    
    name = name or func.__name__
    
    def config_command(func: Callable) -> Optional[Callable]:
        if name in enabled_commands:
            print(f"command '{name}' is enabled!")
            return command(name=name)(func)
        else:
            print(f"command '{name}' is disabled!")
            return None
        
    return config_command
