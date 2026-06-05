import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from meetings.models import Meeting, MeetingMember
from accounts.models import UserProfile
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.meeting_id = self.scope['url_route']['kwargs']['meeting_id']
        self.room_group_name = f'chat_{self.meeting_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        # Check if the user is a member of the meeting
        is_member = await self.check_meeting_membership(self.meeting_id, self.user)
        if not is_member:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        content = data.get('content', '').strip()
        if not content:
            return

        # Save message to database
        message, sender_nickname = await self.save_message(self.meeting_id, self.user, content)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': message.id,
                'sender_id': self.user.id,
                'sender_nickname': sender_nickname,
                'content': message.content,
                'sent_at': message.sent_at.isoformat()
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        is_mine = event['sender_id'] == self.user.id
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'sender': {
                'nickname': event['sender_nickname']
            },
            'content': event['content'],
            'sent_at': event['sent_at'],
            'is_mine': is_mine
        }))

    @database_sync_to_async
    def check_meeting_membership(self, meeting_id, user):
        try:
            profile = user.userprofile
            return MeetingMember.objects.filter(meeting_id=meeting_id, user=profile).exists()
        except UserProfile.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, meeting_id, user, content):
        meeting = Meeting.objects.get(id=meeting_id)
        profile = user.userprofile
        message = ChatMessage.objects.create(
            meeting=meeting,
            sender=profile,
            content=content
        )
        return message, profile.nickname
