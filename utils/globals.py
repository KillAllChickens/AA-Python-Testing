class GlobalBotState:
    _instance = None
    bot = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_var(self, value):
        self.bot = value

    def get_var(self):
        return self.bot

global_bot = GlobalBotState()
