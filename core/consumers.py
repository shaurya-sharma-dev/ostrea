import json
from channels.generic.websocket import AsyncWebsocketConsumer

ACTIVE_ROOM_CONNECTIONS = {}

class TransferConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        self.my_session_id = self.channel_name 

        if self.room_id not in ACTIVE_ROOM_CONNECTIONS:
            ACTIVE_ROOM_CONNECTIONS[self.room_id] = 0

        if ACTIVE_ROOM_CONNECTIONS[self.room_id] >= 2:
            await self.close(code=4001)
            return

        ACTIVE_ROOM_CONNECTIONS[self.room_id] += 1

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        await self.send(text_data=json.dumps({
            "type": "connected",
            "your_session_id": self.my_session_id
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "room_id") and self.room_id in ACTIVE_ROOM_CONNECTIONS:
            ACTIVE_ROOM_CONNECTIONS[self.room_id] -= 1
            
            if ACTIVE_ROOM_CONNECTIONS[self.room_id] <= 0:
                ACTIVE_ROOM_CONNECTIONS.pop(self.room_id, None)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "peer_disconnected",
                "sender_id": self.my_session_id
            }
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "relay",
                "payload": text_data,
                "sender_id": self.my_session_id
            }
        )

    async def relay(self, event):
        if event["sender_id"] == self.my_session_id:
            return

        await self.send(text_data=event["payload"])

    async def peer_disconnected(self, event):
        await self.send(text_data=json.dumps({
            "type": "peer_disconnected",
        }))
        await self.close(code=4002)