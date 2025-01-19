import asyncio
import websockets
from typing import Optional
from .bot import Bot
# import threading
from .globals import global_bot
from .bot_utils import load_cogs
class WebSocketServer:
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WebSocketServer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, host: str="127.0.0.1", port: int=8765):
        self.host = host
        self.port = port
        # self.client = None
        self.response_queue = asyncio.Queue()
        self.processable_packets = ["send_message", "end_python", "start_twitch", "load_config"]
        self.stop_event = asyncio.Event()
        self.ready_event = asyncio.Event()
        self.bot = None
        # self.bot = None
        self.bot = global_bot.get_var()
    
    async def start_server(self):
        asyncio.create_task(self.run_check_self_bot_task())
        async with websockets.serve(self.handle_client, self.host, self.port):
            self.ready_event.set()
            await self.stop_event.wait()
        
    async def handle_client(self, websocket):
        print("Client Connected")
        self.client = websocket
        print(self.client)
        try:
            async for message in websocket:
                # print(self.client) # Prints <websockets.asyncio.server.ServerConnection object at 0x751459894d70> which is good
                self.client = websocket
                await self.send_message("ACK:Unknown")
                print(f"Recieved Message: {message}")
                command_invoked = message.strip().split(":")[0]
                print(f"Recieved Command: {command_invoked}")
                if command_invoked in self.processable_packets:
                    print("\tmessage is processable processing")
                    await self.bot.process_packet(message.strip())
                    # if command_invoked == "load_config":
                    #     if self.bot is not None:
                    #         await load_cogs(self.bot)
                else:
                    print("\tmessage is NOT processable, forwarding message...")
                    await self.response_queue.put(message.strip())
                
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
        finally:
            print("Cleaning up client.")
            self.client = None
            await websocket.close()
            print("WebSocket connection closed.")

    
    async def send_message(self, message):
        # print(f"Sending message: {message}")
        if self.client:
            await self.client.send(message)
        else:
            print("Client doesnt exist")
    
    async def send_message_with_username(self, message: str, username: str, *additionals: Optional[str]):
        # print()
        if self.client:
            await self.client.send(f"{message}:{username}" + (":" + ":".join(additionals) if additionals else ""))
        else:
            print("Client doesnt exist:")
        
    async def wait_for_response(self):
        response = await self.response_queue.get()
        return response
    
    async def check_self_bot(self):
        if not self.bot:
            self.bot = global_bot.get_var()

    async def run_check_self_bot_task(self):
        """Runs check_self_bot every 2 seconds."""
        while not self.stop_event.is_set():
            await self.check_self_bot()
            await asyncio.sleep(2)
            
    # async def start_bot_instance(self):
    #     if not self.bot:
    #         self.bot = await asyncio.to_thread(self.create_bot_instance)
    
    # def create_bot_instance(self):
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     return Bot()