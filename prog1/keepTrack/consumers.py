import json

from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import *
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        comment = await self.save_data(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': comment
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'info':'comment',
            'message': message
        }))

    async def delete_comment(self, event):
        comment = event['message']
        # print("en")
        await self.send(text_data=json.dumps({
            'info':'delete',
            'comment': comment
        }))

    async def modify_comment(self, event):
        comment = event['message']
        # print("en")
        await self.send(text_data=json.dumps({
            'info':'edit',
            'comment': comment
        }))

    @database_sync_to_async
    def save_data(self, data):
        serializer = CommentCSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        x = serializer.create(serializer.validated_data)   

        data = CommentCSerializer(x).data 
        usr = UserSerializer(instance=Users.objects.get(id=data['sender']))
        data['sender'] = usr.data
        return data

    