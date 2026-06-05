from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
import json

from .models import ChatMessage
from meetings.models import Meeting, MeetingMember
from .serializers import ChatMessageSerializer

# 일반 Django 뷰
@login_required
def meeting_chat_view(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    # 해당 모임의 멤버인지 확인 (선택적)
    if not MeetingMember.objects.filter(meeting=meeting, user=request.user.userprofile).exists():
        # 멤버가 아니라면 입장을 막거나 리다이렉트
        return redirect('meeting_list')
    
    # 초기 메시지 로드 (select_related로 N+1 쿼리 최적화)
    initial_messages = ChatMessage.objects.filter(meeting=meeting).select_related('sender__user').order_by('sent_at')
    serializer = ChatMessageSerializer(initial_messages, many=True, context={'request': request})
    
    # 모임 멤버 목록
    members = MeetingMember.objects.filter(meeting=meeting).select_related('user')
    
    return render(request, 'chat/chat.html', {
        'meeting': meeting,
        'initial_messages_json': json.dumps(serializer.data),
        'members': members
    })
