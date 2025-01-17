# Scratchpad
Here I will jot random notes to help myself understand things.

## Global configuration...
To do this I need to redesign the bot-loading logic, to instead first load the conifg first then later initialize the bot with `username` and `command_prefix` set the rest of the logic *should* be fine. Like just change the `Config` class(s) to read new keys instead of new files, which should be easy.  
  
I will need to reqork more than thought, right now the websocket is the last thing to start, but for this to work godot will have to send a packet telling where the global config file is(maybe something like: `load_config:/path/to/config.json`), so the websocket should be the first to load in order to catch this packet. 

## pyinstaller issues...
due to line 8 in `utils/bot_utils.py` the compiled executable requires a folder named `commands` with valid python files inside, one way to get around this would be to embed the commands outside of cogs inside of `main.py` or `utils/bot.py` but that may require too much effort, there must be a better way...