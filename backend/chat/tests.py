from django.contrib.auth.models import User
from django.test import TransactionTestCase
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.db import database_sync_to_async
from meetings.models import Meeting, MeetingMember
from chat.routing import websocket_urlpatterns
from chat.models import ChatMessage
import datetime

class MockAuthMiddleware:
    """Mock Middleware to inject a test user into Channels scope['user']"""
    def __init__(self, inner, user):
        self.inner = inner
        self.user = user

    async def __call__(self, scope, receive, send):
        scope['user'] = self.user
        return await self.inner(scope, receive, send)

class ChatWebSocketTests(TransactionTestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        
        # Get profiles (created via signals)
        self.profile1 = self.user1.userprofile
        self.profile2 = self.user2.userprofile
        
        # Create meeting
        self.meeting = Meeting.objects.create(
            host=self.profile1,
            category='운동',
            title='테스트 모임',
            description='테스트 설명',
            location={'name': '서울역', 'lat': '37.5546', 'lng': '126.9706'},
            schedule=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        
        # Add user1 (host) as member
        MeetingMember.objects.create(meeting=self.meeting, user=self.profile1)

    async def test_member_can_connect_and_chat(self):
        # Inject self.user1 who is a member of the meeting
        test_app = MockAuthMiddleware(
            URLRouter(websocket_urlpatterns),
            user=self.user1
        )
        
        # Connect to WebSocket
        communicator = WebsocketCommunicator(test_app, f"/ws/chat/{self.meeting.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Send message
        await communicator.send_json_to({"content": "안녕하세요"})
        
        # Receive message (it broadcasts to room group, so communicator receives it)
        response = await communicator.receive_json_from()
        self.assertEqual(response['content'], "안녕하세요")
        self.assertEqual(response['sender']['nickname'], self.profile1.nickname)
        self.assertTrue(response['is_mine'])
        
        # Verify message is saved to DB
        @database_sync_to_async
        def get_messages():
            return list(ChatMessage.objects.filter(meeting=self.meeting))
            
        messages = await get_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, "안녕하세요")
        
        # Disconnect
        await communicator.disconnect()

    async def test_non_member_cannot_connect(self):
        # Inject self.user2 who is NOT a member of the meeting
        test_app = MockAuthMiddleware(
            URLRouter(websocket_urlpatterns),
            user=self.user2
        )
        
        communicator = WebsocketCommunicator(test_app, f"/ws/chat/{self.meeting.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)  # Connection should be denied

    async def test_unauthenticated_cannot_connect(self):
        from django.contrib.auth.models import AnonymousUser
        # Inject AnonymousUser (unauthenticated)
        test_app = MockAuthMiddleware(
            URLRouter(websocket_urlpatterns),
            user=AnonymousUser()
        )
        
        communicator = WebsocketCommunicator(test_app, f"/ws/chat/{self.meeting.id}/")
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)  # Connection should be denied
