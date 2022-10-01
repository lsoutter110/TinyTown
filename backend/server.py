import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)

@dataclass
class Client:
	ws: WebSocketServerProtocol
	pair: int = None


class Server:
	waiting = None
	client_pairs = []

	async def register(self, ws: WebSocketServerProtocol) -> None:
		logging.info(f"{ws.remote_address} connects.")
		if(self.waiting == None):
			self.waiting = ws
			logging.info(f"In queue")
		else:
			self.client_pairs.append([self.waiting, ws])

			await ws.send("s")
			await self.waiting.send("s")

			self.waiting = None
			logging.info(f"Pair created in list {self.client_pairs}")

	async def unregister(self, ws: WebSocketServerProtocol) -> None:
		if(ws == self.waiting):
			self.waiting = None
		else:
			for pair in self.client_pairs:
				if(ws in pair):
					self.client_pairs.remove(pair)
		logging.info(f"{ws.remote_address} disconnects.")

	async def ws_handler(self, ws:WebSocketServerProtocol, url: str) -> None:
		await self.register(ws)
		try:
			await self.run_game(ws)
		finally:
			await self.unregister(ws)

	async def run_game(self, ws: WebSocketServerProtocol) -> None:
		async for message in ws:
			partner = find_partner(self.client_pairs, ws)
			if(partner != None):
				logging.info(f"{message} recieved from {ws.remote_address}, sent to {partner.remote_address}")
				await partner.send(message)
			else:
				logging.info(f"{message} sent from {ws.remote_address} not in pair")



#HELPER FUNCTIONS

def find_partner(pairs, ws: WebSocketServerProtocol):
	for pair in pairs:
		if(pair[0] == ws):
			return pair[1]
		if(pair[1] == ws):
			return pair[0]
		return None

server = Server()
start_server = websockets.serve(server.ws_handler, "localhost", 4000)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()
