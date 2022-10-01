import asyncio
import logging
import websockets
#from websockets import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)

async def consume(hostname: str, port: int) -> None:
	websocket_resource_url = f"ws://{hostname}:{port}"
	async with websockets.connect(websocket_resource_url) as websocket:
		while True:
			message = await websocket.recv()
			log_message(message)
			if(message == "start_build"):
				input("")
				await websocket.send("built")
			if("built" in message):
				
				await websocket.send("attacked" + input(""))
			if("attacked" in message):
				
				await websocket.send("built" + input(""))

def log_message(message: str) -> None:
	logging.info(f"Message: {message}")

def main():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(consume(hostname="localhost", port=4000))
	loop.run_forever()

if(__name__ == "__main__"):
	main()
