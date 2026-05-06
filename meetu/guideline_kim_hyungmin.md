# **🟣 김형민 — PR#1 (~발표 전까지)**

## **담당 영역**

Google OAuth 인증 시스템 + 유저 프로필 모델 + 모임 생성 기초

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
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` 등 구글 OAuth 키는 단톡방/노션에 공유된 값을 복사해서 채워주세요.
- `KAKAO_MAP_API_KEY`도 단톡방 참고.

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

## **PR#1 할 일 (8가지)**

⚠️ **이 PR은 가장 먼저 머지되어야 합니다.** 다른 팀원(박성진, 임태규)이 이 모델과 뷰를 import해서 작업하기 때문입니다.

| # | 항목 | 파일 경로 |
| --- | --- | --- |
| 1 | 구글 로그인 버튼 UI | `meetu/backend/templates/socialaccount/login.html` |
| 2 | 유저 프로필 모델 | `meetu/backend/accounts/models.py` |
| 3 | 구글 로그인 시 자동 프로필 생성 | `meetu/backend/accounts/signals.py` |
| 4 | 계정 뷰 (랜딩 페이지 + 프로필) | `meetu/backend/accounts/views.py` |
| 5 | 계정 URL 연결 | `meetu/backend/accounts/urls.py` |
| 6 | 모임 기초 모델 설계 | `meetu/backend/meetings/models.py` |
| 7 | 모임 생성 뷰 로직 | `meetu/backend/meetings/views.py` |
| 8 | 모임 생성 URL 연결 | `meetu/backend/meetings/urls.py` |

### **브랜치 생성**

```bash
git checkout develop
git pull
git checkout -b feat/auth-and-meeting-creation
```

---

## **1. 구글 로그인 버튼 UI**

### **체크리스트**
- [ ] Google 로그인 버튼 클릭 시 OAuth 인증 페이지로 이동
- [ ] 로그인 완료 후 `/meetings/` 페이지로 리다이렉트

### **참고 코드/구조**
**파일 경로**: `meetu/backend/templates/socialaccount/login.html`

```html
{% extends "base.html" %}

{% block content %}
<div class="max-w-md mx-auto px-4 py-20 flex flex-col items-center justify-center min-h-[70vh]">
    <div class="surface p-10 rounded-2xl w-full text-center shadow-lg border border-white/5">
        <div class="w-20 h-20 mx-auto bg-white rounded-full flex items-center justify-center mb-6 shadow-md">
            <!-- Google "G" Logo SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="40px" height="40px">
                <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
                <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
                <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
                <path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
            </svg>
        </div>
        
        <h1 class="text-2xl font-bold mb-3 text-white">구글로 계속하기</h1>
        <p class="text-gray-400 mb-8 text-sm">안전하고 간편하게 Gachi에 로그인합니다.</p>
        
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 rounded-xl text-white font-bold text-lg transition-colors btn-glow">
                계속하기
            </button>
        </form>
    </div>
</div>
{% endblock %}
```

---

## **2. 유저 프로필 모델**

### **체크리스트**
- [ ] Django User와 1:1 연결되는 UserProfile 모델 생성
- [ ] 닉네임, 매너온도(기본값 36.5), 즐겨찾기 필드 포함
- [ ] 이메일은 다른 사용자에게 절대 노출되지 않도록 설계

### **참고 코드/구조**
**파일 경로**: `meetu/backend/accounts/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, unique=True)
    manner = models.FloatField(default=36.5)
    favorites = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.nickname
```

---

## **3. 구글 로그인 시 자동 프로필 생성 (시그널)**

### **체크리스트**
- [ ] 최초 로그인 시 닉네임 자동 생성 (예: `user_abcdef`)
- [ ] 같은 Google 이메일로 재로그인 시 새 계정 생성 없이 기존 계정 연결

### **참고 코드/구조**
**파일 경로**: `meetu/backend/accounts/signals.py`

```python
from allauth.socialaccount.signals import social_account_added
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
import random, string

def generate_nickname():
    return 'user_' + ''.join(random.choices(string.ascii_lowercase, k=6))

@receiver(post_save, sender=User)
def create_profile_on_user_save(sender, instance, created, **kwargs):
    if created and not UserProfile.objects.filter(user=instance).exists():
        UserProfile.objects.create(user=instance, nickname=generate_nickname())

@receiver(social_account_added)
def create_profile(request, sociallogin, **kwargs):
    user = sociallogin.user
    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user, nickname=generate_nickname())
```

---

## **4. 계정 뷰 (랜딩 페이지 + 프로필)**

### **체크리스트**
- [ ] 루트(`/`) 접속 시 로그인 여부에 따라 분기 (로그인 → 모임 목록 / 비로그인 → 랜딩 페이지)
- [ ] 내 프로필 페이지에서 닉네임, 매너온도, 참여 모임 이력, 즐겨찾기 표시
- [ ] 다른 유저 상세 프로필 + 즐겨찾기 추가/해제

### **참고 코드/구조**
**파일 경로**: `meetu/backend/accounts/views.py`

```python
from django.views.generic import TemplateView
from django.shortcuts import redirect

class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/meetings/')
        return super().get(request, *args, **kwargs)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from meetings.models import MeetingMember

@login_required
def profile_view(request):
    profile = request.user.userprofile
    past_meetings = MeetingMember.objects.filter(user=profile).select_related('meeting').order_by('-joined_at')
    favorites = profile.favorites.all()
    
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'past_meetings': past_meetings,
        'favorites': favorites
    })

@login_required
def user_detail_view(request, user_id):
    target_profile = get_object_or_404(UserProfile, user__id=user_id)
    is_favorite = request.user.userprofile.favorites.filter(id=target_profile.id).exists()
    
    return render(request, 'accounts/user_detail.html', {
        'target_profile': target_profile,
        'is_favorite': is_favorite
    })

@login_required
def toggle_favorite(request, user_id):
    if request.method == 'POST':
        target_profile = get_object_or_404(UserProfile, user__id=user_id)
        my_profile = request.user.userprofile
        
        if target_profile in my_profile.favorites.all():
            my_profile.favorites.remove(target_profile)
        else:
            my_profile.favorites.add(target_profile)
            
    return redirect('user_detail', user_id=user_id)
```

---

## **5. 계정 URL 연결**

### **참고 코드/구조**
**파일 경로**: `meetu/backend/accounts/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('profile/<int:user_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
```

---

## **6. 모임 기초 모델 설계**

### **체크리스트**
- [ ] 카테고리(운동/게임/스터디/식사) 선택 가능
- [ ] 모임 제목, 상세 내용, 위치(JSON), 일정, 정원(기본 4명) 필드 구현
- [ ] MeetingMember 모델로 참가자 관리

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/models.py`

```python
from django.db import models
from accounts.models import UserProfile

class Meeting(models.Model):
    CATEGORY_CHOICES = [('운동','운동'), ('게임','게임'), ('스터디','스터디'), ('식사','식사')]
    host = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100, default="새로운 모임")
    description = models.TextField(blank=True, null=True)
    location = models.JSONField(default=dict, blank=True)
    schedule = models.DateTimeField(null=True, blank=True)
    max_members = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

class MeetingMember(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
```

---

## **7. 모임 생성 뷰 로직**

### **체크리스트**
- [ ] 카테고리, 제목, 내용을 입력하여 모임 개설
- [ ] 모임 생성 시 호스트가 자동으로 첫 번째 멤버로 등록
- [ ] 생성 완료 후 모임 목록 페이지로 리다이렉트

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/views.py`

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Meeting, MeetingMember

@login_required
def meeting_create(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if category in dict(Meeting.CATEGORY_CHOICES) and title:
            meeting = Meeting.objects.create(
                host=request.user.userprofile,
                category=category,
                title=title,
                description=description
            )
            # 모임을 생성한 사람을 자동으로 첫 멤버로 등록
            MeetingMember.objects.create(meeting=meeting, user=request.user.userprofile)
            return redirect('meeting_list')
            
    return render(request, 'meetings/meeting_create.html')
```

---

## **8. 모임 생성 URL 연결**

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.meeting_create, name='meeting_create'),
]
```

---

## **커밋 + PR**

작업을 논리적인 커밋으로 분리해서 올리는 걸 권장합니다:

```bash
# 커밋 1: 인증 + 유저 모델
git add meetu/backend/accounts/ meetu/backend/templates/socialaccount/
git commit -m "feat: Google OAuth 로그인 및 유저 프로필 구현 (#20, #21)"

# 커밋 2: 모임 생성
git add meetu/backend/meetings/
git commit -m "feat: 모임 생성 모델 및 뷰 구현 (#22)"

git push -u origin feat/auth-and-meeting-creation
```

**GitHub에서**:
1. "Compare & pull request" 버튼 클릭
2. ⚠️ Base branch를 **develop**으로 설정 (main 아님!)
3. 제목: `feat: PR#1 Google 로그인 및 모임 생성 기초`
4. 리뷰어(Reviewers) 지정 및 리뷰 요청

---

## **증빙 (Progress Report용)**

단톡방/이슈 코멘트에 다음 내용을 공유해주세요:
- [ ] 📸 Google 로그인 화면 및 로그인 성공 후 리다이렉트 화면 스크린샷
- [ ] 📸 DB에서 User / UserProfile 테이블 데이터 확인 스크린샷
- [ ] 📸 모임 생성 폼 입력 → 저장 성공 스크린샷
- [ ] 🔖 본인 Commit ID

---

## **❓ 막히면**

- **구글 로그인 시 `redirect_uri_mismatch` 에러** → 구글 클라우드 콘솔 > 승인된 리디렉션 URI에 `http://localhost:8000/accounts/google/login/callback/` 등록 확인
- **`allauth` 관련 import 에러** → `pip install django-allauth` 확인, `settings.py`의 `INSTALLED_APPS`에 allauth 관련 앱 등록 확인
- **`makemigrations` 시 에러** → `accounts` 앱 먼저 마이그레이션 후 `meetings` 앱 마이그레이션 (의존성 순서)
- **2시간 이상 막히면** → 혼자 끙끙대지 말고 바로 단톡방/이슈에 질문 남기기 🙏

---

## **🤝 팀원 제공 일정 (인터페이스 계약)**

| 제공 시점 | 산출물 | 수신자 | 용도 |
| --- | --- | --- | --- |
| **최우선 (가장 먼저 PR)** | `UserProfile`, `Meeting`, `MeetingMember` 모델 코드 | 박성진, 임태규 | 두 팀원이 이 모델을 import해서 각자 뷰/로직 작성 |
| **PR 머지 직후** | 로그인 가능한 환경 | 전체 | 박성진, 임태규가 테스트 시 "로그인된 상태" 필요 |
