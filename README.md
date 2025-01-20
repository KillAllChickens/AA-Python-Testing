# TwitchIntegration
**BEFORE COMPILING:** Set the variable `compile_mode` in `utils/bot_utils.py` to be `True` otherwise the pyinstaller compiled code will not work!  
After you have done the above use this command to compile: `pyinstaller --onefile main.py --add-data "commands:commands" --add-data "utils:utils"`.  

to install all required libraries use `pip install -r requirements.txt`  
  
~~to update libraries `rm -rf requirements.txt` then generate it again with `pipreqs`.~~  