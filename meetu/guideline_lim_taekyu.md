# **🔵 임태규 — PR#1 (~발표 전까지)**

## **담당 영역**

모임 참가 로직 + 인앱 실시간 채팅 (Long Polling)

---

## **환경 세팅 (처음 한 번만)**

### **1. Repo clone**

```bash
git clone https://github.com/Eisenberg1113/SWE_Group4.git
cd SWE_Group4
git checkout develop
git pull
```

### **2. `.env` 파일 생성**

```bash
cp meetu/.env.example meetu/.env
```
- 환경 변수 설정에 필요한 값들은 단톡방/노션을 참고하여 채워주세요.

### **3. 실행 환경 구성**

```bash
# 가상환경 생성 및 실행
python -m venv venv
source venv/bin/activate
pip install -r meetu/backend/requirements.txt

# DB 마이그레이션 및 실행
cd meetu/backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## **PR#1 할 일 (7가지)**

⚠️ **김형민 PR, 박성진 PR이 먼저 머지되어야 합니다.** 김형민이 만든 모델과 박성진이 만든 목록 페이지의 "참여하기" 버튼을 이어받아서 작업합니다.

| # | 항목 | 파일 경로 |
| --- | --- | --- |
| 1 | 모임 참가 뷰 (`meetings/views.py`에 추가) | `meetu/backend/meetings/views.py` |
| 2 | 모임 참가/채팅 URL 추가 | `meetu/backend/meetings/urls.py` |
| 3 | 채팅 메시지 모델 | `meetu/backend/chat/models.py` |
| 4 | 채팅 메시지 Serializer | `meetu/backend/chat/serializers.py` |
| 5 | 채팅 뷰 (페이지 렌더링 + Long Polling API) | `meetu/backend/chat/views.py` |
| 6 | 채팅 API URL 연결 | `meetu/backend/chat/urls.py` |
| 7 | 채팅방 프론트엔드 | `meetu/backend/templates/chat/chat.html` |

### **브랜치 생성**

```bash
git checkout develop
git pull
git checkout -b feat/meeting-join-and-chat
```

---

## **1. 모임 참가 뷰**

### **체크리스트**
- [ ] 이미 멤버인 경우 바로 채팅방으로 이동
- [ ] 정원(기본 4명)이 가득 찬 모임에는 참여 불가 + 에러 메시지 표시
- [ ] 참가 후 자동으로 채팅방으로 이동

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/views.py`
> 박성진이 만든 파일을 열어서 **맨 아래에** 아래 함수를 추가합니다.

```python
@login_required
def meeting_join(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    profile = request.user.userprofile
    
    # 이미 멤버인 경우 바로 채팅방으로 이동
    if MeetingMember.objects.filter(meeting=meeting, user=profile).exists():
        return redirect('meeting_chat', meeting_id=meeting.id)
    
    # 정원 초과 확인
    if meeting.members.count() >= meeting.max_members:
        from django.contrib import messages
        messages.error(request, '이 모임은 이미 정원이 가득 찼습니다.')
        return redirect('meeting_list')
    
    # 멤버로 등록 후 채팅방으로 이동
    MeetingMember.objects.create(meeting=meeting, user=profile)
    return redirect('meeting_chat', meeting_id=meeting.id)
```

---

## **2. 모임 참가/채팅 URL 추가**

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/urls.py`
> 박성진이 만든 파일을 열어서 **전체 교체**합니다.

```python
from django.urls import path
from . import views
from chat.views import meeting_chat_view

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('create/', views.meeting_create, name='meeting_create'),
    path('<int:meeting_id>/join/', views.meeting_join, name='meeting_join'),
    path('<int:meeting_id>/chat/', meeting_chat_view, name='meeting_chat'),
]
```

---

## **3. 채팅 메시지 모델**

### **체크리스트**
- [ ] 모임별 채팅 메시지 저장
- [ ] 보낸 사람(sender), 내용(content), 전송 시간(sent_at) 필드

### **참고 코드/구조**
**파일 경로**: `meetu/backend/chat/models.py` (새로 생성)

```python
from django.db import models
from accounts.models import UserProfile
from meetings.models import Meeting

class ChatMessage(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']
```

---

## **4. 채팅 메시지 Serializer**

### **체크리스트**
- [ ] 내 메시지/상대 메시지 구분을 위한 `is_mine` 필드 포함
- [ ] 보낸 사람 닉네임 표시

### **참고 코드/구조**
**파일 경로**: `meetu/backend/chat/serializers.py` (새로 생성)

```python
from rest_framework import serializers
from .models import ChatMessage

class SenderSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id')
    nickname = serializers.CharField()

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'content', 'sent_at', 'is_mine']

    def get_is_mine(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return obj.sender == request.user.userprofile
        return False
```

---

## **5. 채팅 뷰 (페이지 렌더링 + Long Polling API)**

### **체크리스트**
- [ ] 채팅방 입장 시 이전 메시지 기록 표시
- [ ] 메시지 전송 시 다른 멤버에게 실시간 표시 (Long Polling)
- [ ] 모임 멤버가 아닌 사용자는 채팅방 입장 불가

### **참고 코드/구조**
**파일 경로**: `meetu/backend/chat/views.py` (새로 생성)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
import time

from .models import ChatMessage
from meetings.models import Meeting, MeetingMember
from .serializers import ChatMessageSerializer

# 일반 Django 뷰 — 채팅방 페이지 렌더링
@login_required
def meeting_chat_view(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if not MeetingMember.objects.filter(meeting=meeting, user=request.user.userprofile).exists():
        return redirect('meeting_list')
    
    initial_messages = ChatMessage.objects.filter(meeting=meeting).order_by('sent_at')
    serializer = ChatMessageSerializer(initial_messages, many=True, context={'request': request})
    
    import json
    members = MeetingMember.objects.filter(meeting=meeting).select_related('user')
    
    return render(request, 'chat/chat.html', {
        'meeting': meeting,
        'initial_messages_json': json.dumps(serializer.data),
        'members': members
    })


# DRF API 뷰 — Long Polling 방식 메시지 조회/전송
class MessageAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, meeting_id):
        try:
            last_id = int(request.GET.get('last_id', '0'))
        except ValueError:
            return Response({'error': 'Invalid last_id format'}, status=status.HTTP_400_BAD_REQUEST)

        for _ in range(25):
            messages = ChatMessage.objects.filter(
                meeting_id=meeting_id,
                id__gt=last_id
            ).order_by('id')

            if messages.exists():
                serializer = ChatMessageSerializer(messages, many=True, context={'request': request})
                return Response(serializer.data)
            time.sleep(1)

        return Response([], status=status.HTTP_200_OK)

    def post(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, id=meeting_id)
        profile = request.user.userprofile

        if not MeetingMember.objects.filter(meeting=meeting, user=profile).exists():
            return Response({'error': 'Not a member'}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({'error': 'Empty message'}, status=status.HTTP_400_BAD_REQUEST)

        message = ChatMessage.objects.create(
            meeting=meeting,
            sender=profile,
            content=content
        )
        serializer = ChatMessageSerializer(message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

---

## **6. 채팅 API URL 연결**

### **참고 코드/구조**
**파일 경로**: `meetu/backend/chat/urls.py` (새로 생성)

```python
from django.urls import path
from .views import MessageAPIView

urlpatterns = [
    path('meetings/<int:meeting_id>/messages/', MessageAPIView.as_view(), name='message_api'),
]
```

---

## **7. 채팅방 프론트엔드**

### **체크리스트**
- [ ] 내 메시지는 오른쪽, 상대 메시지는 왼쪽 정렬 (색상 차이)
- [ ] 보낸 사람 닉네임과 전송 시간 표시
- [ ] Long Polling으로 실시간 메시지 갱신

### **참고 코드/구조**
**파일 경로**: `meetu/backend/templates/chat/chat.html` (새로 생성)

```html
{% extends "base.html" %}

{% block content %}
<div class="max-w-3xl mx-auto px-4 py-6 flex flex-col" style="height: calc(100vh - 80px);">
    <div class="surface p-4 rounded-2xl mb-4 flex items-center justify-between border border-white/5">
        <div>
            <div class="flex items-center gap-2 mb-1">
                <span class="px-2 py-0.5 bg-indigo-500/20 text-indigo-300 text-xs rounded font-bold">{{ meeting.category }}</span>
                <h1 class="text-xl font-bold">{{ meeting.title }}</h1>
            </div>
            <p class="text-sm text-gray-400">📍 {{ meeting.location.name }} / 🗓️ {{ meeting.schedule|date:"n월 j일 A g:i" }}</p>
        </div>
        <div class="flex flex-col gap-2 items-end">
            <h3 class="text-sm text-gray-300 font-bold mb-1">참여자 목록</h3>
            <div class="flex flex-wrap gap-2 justify-end">
                {% for member in members %}
                <div class="flex items-center gap-2 bg-gray-800 px-3 py-1.5 rounded-lg border border-white/5">
                    <span class="text-sm text-cyan-400 font-medium">{{ member.user.nickname }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <div id="message-list" class="flex-grow overflow-y-auto py-4 space-y-6"></div>

    <div class="flex-shrink-0 pt-4 border-t border-white/10">
        <form id="chat-form" class="flex items-center gap-4">
            <input type="text" id="message-input" class="surface w-full p-3 rounded-lg border-transparent focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="메시지를 입력하세요..." autocomplete="off" required>
            <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition-colors">전송</button>
        </form>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const messageList = document.getElementById('message-list');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const meetingId = {{ meeting.id }};
    const apiEndpoint = `/api/meetings/${meetingId}/messages/`;
    let lastMessageId = 0;

    const initialMessages = {{ initial_messages_json|safe }};
    initialMessages.forEach(addMessageToDOM);
    scrollToBottom();
    pollForNewMessages();

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (content) { sendMessage(content); messageInput.value = ''; }
    });

    function addMessageToDOM(message) {
        const messageWrapper = document.createElement('div');
        const messageElement = document.createElement('div');
        const sentAt = new Date(message.sent_at).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' });
        const alignment = message.is_mine ? 'justify-end' : 'justify-start';
        const bgColor = message.is_mine ? 'bg-indigo-600' : 'surface';
        const textColor = message.is_mine ? 'text-white' : 'text-gray-200';
        messageWrapper.className = `flex ${alignment}`;
        messageElement.className = `p-3 rounded-xl max-w-lg ${bgColor} ${textColor}`;
        messageElement.innerHTML = `
            <div class="flex items-end gap-2">
                <div>
                    ${!message.is_mine ? `<div class="text-xs text-cyan-400 font-bold mb-1">${message.sender.nickname}</div>` : ''}
                    <p class="text-base">${message.content}</p>
                </div>
                <div class="text-xs text-gray-500 flex-shrink-0">${sentAt}</div>
            </div>
        `;
        messageWrapper.appendChild(messageElement);
        messageList.appendChild(messageWrapper);
        if (message.id > lastMessageId) lastMessageId = message.id;
    }

    function scrollToBottom() { messageList.scrollTop = messageList.scrollHeight; }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    async function sendMessage(content) {
        try {
            await fetch(apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
                body: JSON.stringify({ content: content })
            });
        } catch (error) { console.error('Error sending message:', error); }
    }

    async function pollForNewMessages() {
        try {
            const response = await fetch(`${apiEndpoint}?last_id=${lastMessageId}`);
            if (response.status === 200) {
                const newMessages = await response.json();
                if (newMessages.length > 0) { newMessages.forEach(addMessageToDOM); scrollToBottom(); }
            }
        } catch (error) {
            console.error('Polling error:', error);
            setTimeout(pollForNewMessages, 5000);
            return;
        }
        pollForNewMessages();
    }
});
</script>
{% endblock %}
```

---

## **커밋 + PR**

```bash
# 커밋 1: 모임 참가
git add meetu/backend/meetings/
git commit -m "feat: 모임 참가 로직 구현 (#26)"

# 커밋 2: 채팅 시스템
git add meetu/backend/chat/ meetu/backend/templates/chat/
git commit -m "feat: 인앱 실시간 채팅 구현 (Long Polling) (#27)"

git push -u origin feat/meeting-join-and-chat
```

**GitHub에서**:
1. "Compare & pull request" 버튼 클릭
2. ⚠️ Base branch를 **develop**으로 설정 (main 아님!)
3. 제목: `feat: PR#1 모임 참가 + 인앱 채팅`
4. 리뷰어(Reviewers) 지정 및 리뷰 요청


---

## **🤝 팀원 제공 일정 (인터페이스 계약)**

| 제공 시점 | 산출물 | 수신자 | 용도 |
| --- | --- | --- | --- |
| **PR 머지 직후** | 채팅 시스템 + Long Polling API | 전체 | 세 명의 PR이 모두 합쳐지면 Release 1+2 핵심 기능 완성 |
| **Release 3 시작 시** | 채팅방 내 매너 평가 버튼 추가 | Release 3 담당자 | US-09 매너온도 평가 기능 연결 |
