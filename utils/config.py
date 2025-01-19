import json
from typing import Optional, Union, List

class Config:
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.get_config()
        self.client_id = self.config.get("client_id") if self.config else None
        self.client_secret = self.config.get("client_secret") if self.config else None
        self.access_token = self.config.get("access_token") if self.config and self.config.get("access_token") != "" else ""
        self.refresh_token = self.config.get("refresh_token") if self.config and self.config.get("refresh_token") != "" else None
        

    def get_config(self) -> dict:
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}")
            return {}

    def set_val(self, key: str, new_val: str) -> None:
        if not self.config:
            self.config = {}
            
        self.config[key] = new_val
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            # print(f"Updated '{key}' to '{new_val}' in the config.")
            
            if key == "access_token":
                self.access_token = new_val
            elif key == "refresh_token":
                self.refresh_token = new_val
        except (IOError, TypeError) as e:
            print(f"Error writing to config file: {e}")

    def get_json_data(self, file_path: str):
        with open(file_path, "r") as f:
            return json.load(f)
        
class CommandConfig:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config_file_dict = {}
        self.enabled_categories = []
        self.all_categories = []
        self.enabled_commands = []
        self.all_commands = []
        self._load_config()

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            self.config_file_dict = json.load(file)

        self.enabled_categories = [
            category for category, details in self.config_file_dict.get("categories", {}).items()
            if details.get("enabled", False)
        ]
        
        self.all_categories = [
            category for category, details in self.config_file_dict.get("categories", {}).items()
        ]
        
        self.enabled_commands = []
        self.all_commands = []
        for command, details in self.config_file_dict.get("commands", {}).items():
            self.all_commands.append(command)
            if details.get("enabled") is not None:
                if details["enabled"]:
                    self.enabled_commands.append(command)
            else:
                categories = details.get("categories", [])
                if all(cat in self.enabled_categories for cat in categories):
                    self.enabled_commands.append(command)


class GlobalConfig:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    

    def __init__(self):#, config_file: str = "config.json"):
        self.config_file = None
        self.config = {}

        # Top-level configuration
        self.username = self.config.get("username", "")
        self.command_prefix = self.config.get("command_prefix", "")

        # Auth configuration
        self.auth = self.config.get("auth", {})
        self.client_id = self.auth.get("client_id", "")
        # self.client_secret = self.auth.get("client_secret", "")
        self.access_token = self.auth.get("access_token", "")
        self.refresh_token = self.auth.get("refresh_token", "")

        # Command configuration
        self.command_config = self.config.get("command_config", {})
        self.categories = self.command_config.get("categories", {})
        self.commands = self.command_config.get("commands", {})
        
    # def __setattr__(self, name, value):
    #     # Allow direct assignment to variables only during initialization
    #     if name == "config_file":
    #         # First, update the config_file and reload the config
    #         self.__dict__["config_file"] = value
    #         self.config = self._load_config()  # Reload config
            
    #         # Now update other dependent attributes
    #         self.username = self.config.get("username", "")
    #         self.command_prefix = self.config.get("command_prefix", "")
    #         self.auth = self.config.get("auth", {})
    #         self.client_id = self.auth.get("client_id", "")
    #         self.client_secret = self.auth.get("client_secret", "")
    #         self.access_token = self.auth.get("access_token", "")
    #         self.refresh_token = self.auth.get("refresh_token", "")
    #         self.command_config = self.config.get("command_config", {})
    #         self.categories = self.command_config.get("categories", {})
    #         self.commands = self.command_config.get("commands", {})
    #     else:
    #         # Default behavior for other attributes
    #         super().__setattr__(name, value)


    def _load_config(self) -> dict:
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config file: {e}")
            return {}

    def save_config(self) -> None:
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.config, file, indent=4)
        except IOError as e:
            print(f"Error writing to config file: {e}")

    def update_auth(self, client_id: Optional[str] = None, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        if client_id:
            self.auth["client_id"] = client_id
            self.client_id = client_id
        # if client_secret:
        #     self.auth["client_secret"] = client_secret
        #     self.client_secret = client_secret
        if access_token:
            self.auth["access_token"] = access_token
            self.access_token = access_token
        if refresh_token:
            self.auth["refresh_token"] = refresh_token
            self.refresh_token = refresh_token
        self.config["auth"] = self.auth
        self.save_config()

    def get_enabled_categories(self) -> List[str]:
        return [cat for cat, details in self.categories.items() if details.get("enabled", False)]

    def get_enabled_commands(self) -> List[str]:
        enabled_categories = self.get_enabled_categories()
        enabled_commands = []
        for command, details in self.commands.items():
            if details.get("enabled") is not None:
                if details["enabled"]:
                    enabled_commands.append(command)
            else:
                categories = details.get("categories", [])
                if all(cat in enabled_categories for cat in categories):
                    enabled_commands.append(command)
        return enabled_commands

    def set_category_status(self, category: str, enabled: bool) -> None:
        """Enable or disable a category."""
        if category in self.categories:
            self.categories[category]["enabled"] = enabled
            self.config["command_config"]["categories"] = self.categories
            self.save_config()

    def set_command_status(self, command: str, enabled: Union[bool, None]) -> None:
        """Enable, disable, or reset (None) a command."""
        if command in self.commands:
            self.commands[command]["enabled"] = enabled
            self.config["command_config"]["commands"] = self.commands
            self.save_config()
    
    def set_val(self, key_path: str, value: Union[str, int, bool, dict, list, None]) -> None:
        keys = key_path.split(".")
        config_section = self.config

        # Traverse the dictionary to the second-to-last key
        for key in keys[:-1]:
            if key not in config_section or not isinstance(config_section[key], dict):
                config_section[key] = {}
            config_section = config_section[key]

        # Set the final key's value
        config_section[keys[-1]] = value

        # Save the updated config
        self.save_config()
    
    def set_config_file(self, new_config_file: str) -> None:
        """Method to change the config file and reload the config"""
        self.config_file = new_config_file
        self.config = self._load_config()

        # Update dependent attributes
        self.username = self.config.get("username", "")
        self.command_prefix = self.config.get("command_prefix", "")
        
        self.auth = self.config.get("auth", {})
        self.client_id = self.auth.get("client_id", "")
        # self.client_secret = self.auth.get("client_secret", "")
        self.access_token = self.auth.get("access_token", "")
        # print(f"UPDATED ACCESS TO '{self.access_token}'")
        self.refresh_token = self.auth.get("refresh_token", "")
        self.command_config = self.config.get("command_config", {})
        self.categories = self.command_config.get("categories", {})
        self.commands = self.command_config.get("commands", "")

    def reload_config(self) -> None:
        """Reload the configuration from the file and update the internal state."""
        self.config = self._load_config()

        # Update dependent attributes
        self.username = self.config.get("username", "")
        self.command_prefix = self.config.get("command_prefix", "")
        
        self.auth = self.config.get("auth", {})
        self.client_id = self.auth.get("client_id", "")
        self.access_token = self.auth.get("access_token", "")
        self.refresh_token = self.auth.get("refresh_token", "")
        self.command_config = self.config.get("command_config", {})
        self.categories = self.command_config.get("categories", {})
        self.commands = self.command_config.get("commands", {})
