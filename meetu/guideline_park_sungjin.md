# **🟢 박성진 — PR#1 (~발표 전까지)**

## **담당 영역**

모임 목록 조회/필터링 + 카카오맵 지도 장소 선택 + Flatpickr 타임피커 일정 선택

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
- `KAKAO_MAP_API_KEY`는 단톡방/노션에 공유된 값을 복사해서 채워주세요. (카카오맵 표시에 필수)
- [카카오 디벨로퍼스](https://developers.kakao.com/) > 내 애플리케이션 > 플랫폼에 `http://localhost` 도메인 등록 필수!

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

## **PR#1 할 일 (4가지)**

⚠️ **김형민 PR이 먼저 머지되어야 합니다.** 김형민이 만든 `Meeting` 모델과 `UserProfile` 모델을 import해서 사용하기 때문입니다.

| # | 항목 | 파일 경로 |
| --- | --- | --- |
| 1 | 모임 목록 조회 + 필터링 + 모임 생성 뷰 확장 | `meetu/backend/meetings/views.py` |
| 2 | 모임 목록/생성 URL 업데이트 | `meetu/backend/meetings/urls.py` |
| 3 | 모임 목록 페이지 (카테고리 필터 탭) | `meetu/backend/templates/meetings/meeting_list.html` |
| 4 | 모임 생성 페이지 (카카오맵 + 타임피커) | `meetu/backend/templates/meetings/meeting_create.html` |

### **브랜치 생성**

```bash
git checkout develop
git pull
git checkout -b feat/meeting-list-map-schedule
```

---

## **1. 모임 목록 조회 + 모임 생성 뷰 확장**

### **체크리스트**
- [ ] 전체 모임 목록을 최신순으로 조회
- [ ] 카테고리(전체/운동/게임/스터디/식사) 탭 필터링 구현
- [ ] 모임 생성 시 카카오맵 좌표(lat, lng), 주소, 일정을 함께 저장
- [ ] 카카오맵 API 키를 템플릿 context로 전달

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/views.py`
> 김형민이 만든 파일을 열어서 **전체 교체**합니다.

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from .models import Meeting, MeetingMember
from accounts.models import UserProfile

@login_required
def meeting_list(request):
    category = request.GET.get('category')
    if category:
        meetings = Meeting.objects.filter(category=category).order_by('-created_at')
    else:
        meetings = Meeting.objects.all().order_by('-created_at')
    return render(request, 'meetings/meeting_list.html', {'meetings': meetings, 'current_category': category})

@login_required
def meeting_create(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        place_name = request.POST.get('place_name', '선택된 위치')
        schedule_str = request.POST.get('schedule')

        if category in dict(Meeting.CATEGORY_CHOICES) and lat and lng and schedule_str and title:
            meeting = Meeting.objects.create(
                host=request.user.userprofile,
                category=category,
                title=title,
                description=description,
                location={
                    'name': place_name,
                    'lat': lat,
                    'lng': lng
                },
                schedule=schedule_str
            )
            MeetingMember.objects.create(meeting=meeting, user=request.user.userprofile)
            return redirect('meeting_list')
    
    context = {
        'kakao_map_api_key': settings.KAKAO_MAP_API_KEY
    }
    return render(request, 'meetings/meeting_create.html', context)
```

---

## **2. 모임 URL 업데이트**

### **참고 코드/구조**
**파일 경로**: `meetu/backend/meetings/urls.py`
> 김형민이 만든 파일을 열어서 **전체 교체**합니다.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('create/', views.meeting_create, name='meeting_create'),
]
```

---

## **3. 모임 목록 페이지**

### **체크리스트**
- [ ] 전체 모임이 카드 형태로 표시
- [ ] 각 카드에 제목, 내용, 호스트 닉네임, 장소, 일정, 참여 인원 표시
- [ ] 전체/운동/게임/스터디/식사 탭으로 필터링 가능
- [ ] "참여하기" 버튼 포함 (임태규가 이후 로직 연결 예정)

### **참고 코드/구조**
**파일 경로**: `meetu/backend/templates/meetings/meeting_list.html` (새로 생성)

```html
{% extends "base.html" %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-bold text-white">모임 목록</h1>
        <a href="{% url 'meeting_create' %}" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 rounded-xl text-white font-bold transition btn-glow">
            + 모임 만들기
        </a>
    </div>

    <!-- 카테고리 필터 탭 -->
    <div class="flex gap-2 mb-8 overflow-x-auto pb-2">
        <a href="{% url 'meeting_list' %}" class="px-4 py-2 rounded-full text-sm font-medium transition {% if not current_category %}bg-indigo-600 text-white{% else %}surface text-gray-400 hover:text-white{% endif %}">
            전체
        </a>
        {% for value, label in meetings.0.CATEGORY_CHOICES %}
        <a href="{% url 'meeting_list' %}?category={{ value }}" class="px-4 py-2 rounded-full text-sm font-medium transition {% if current_category == value %}bg-indigo-600 text-white{% else %}surface text-gray-400 hover:text-white{% endif %}">
            {{ label }}
        </a>
        {% endfor %}
    </div>

    <!-- 모임 카드 목록 -->
    {% for meeting in meetings %}
    <div class="surface p-6 rounded-2xl mb-4 border border-white/5">
        <div class="flex items-start justify-between">
            <div>
                <span class="inline-block px-3 py-1 bg-indigo-600/20 text-indigo-400 rounded-full text-xs font-medium mb-2">{{ meeting.category }}</span>
                <h2 class="text-lg font-bold text-white mb-1">{{ meeting.title }}</h2>
                <p class="text-gray-400 text-sm mb-3">{{ meeting.description|default:"설명 없음" }}</p>
                <div class="flex gap-4 text-xs text-gray-500">
                    <span>👤 {{ meeting.host.nickname }}</span>
                    <span>📍 {{ meeting.location.name|default:"미정" }}</span>
                    <span>📅 {{ meeting.schedule|date:"m/d H:i"|default:"미정" }}</span>
                    <span>👥 {{ meeting.members.count }}/{{ meeting.max_members }}명</span>
                </div>
            </div>
            <a href="{% url 'meeting_join' meeting.id %}" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg text-white text-sm font-medium transition">
                참여하기
            </a>
        </div>
    </div>
    {% empty %}
    <div class="text-center py-20 text-gray-500">
        <p class="text-4xl mb-4">🍃</p>
        <p>아직 모임이 없어요. 첫 모임을 만들어보세요!</p>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

---

## **4. 모임 생성 페이지 (카카오맵 + 타임피커)**

### **체크리스트**
- [ ] 카카오맵이 화면에 표시됨
- [ ] 지도 클릭 시 마커 표시 + 해당 위치 주소 자동 표시
- [ ] 선택된 좌표(lat, lng)와 주소가 hidden input으로 저장
- [ ] 날짜+시간 선택 가능한 타임피커 제공 (한국어 로케일)
- [ ] 과거 날짜는 선택 불가

### **참고 코드/구조**
**파일 경로**: `meetu/backend/templates/meetings/meeting_create.html` (새로 생성)

```html
{% extends "base.html" %}

{% block styles %}
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
<link rel="stylesheet" href="https://npmcdn.com/flatpickr/dist/themes/dark.css">
{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-white mb-8">새 모임 만들기</h1>
    <div class="surface p-8 rounded-2xl border border-white/5">
        <form method="post">
            {% csrf_token %}
            
            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-300 mb-3">카테고리 선택</label>
                <div class="grid grid-cols-4 gap-3">
                    <label class="relative cursor-pointer">
                        <input type="radio" name="category" value="운동" class="peer sr-only" required>
                        <div class="surface p-4 rounded-xl text-center peer-checked:bg-indigo-600/20 peer-checked:border-indigo-500 peer-checked:text-indigo-400 transition">운동</div>
                    </label>
                    <label class="relative cursor-pointer">
                        <input type="radio" name="category" value="게임" class="peer sr-only">
                        <div class="surface p-4 rounded-xl text-center peer-checked:bg-indigo-600/20 peer-checked:border-indigo-500 peer-checked:text-indigo-400 transition">게임</div>
                    </label>
                    <label class="relative cursor-pointer">
                        <input type="radio" name="category" value="스터디" class="peer sr-only">
                        <div class="surface p-4 rounded-xl text-center peer-checked:bg-indigo-600/20 peer-checked:border-indigo-500 peer-checked:text-indigo-400 transition">스터디</div>
                    </label>
                    <label class="relative cursor-pointer">
                        <input type="radio" name="category" value="식사" class="peer sr-only">
                        <div class="surface p-4 rounded-xl text-center peer-checked:bg-indigo-600/20 peer-checked:border-indigo-500 peer-checked:text-indigo-400 transition">식사</div>
                    </label>
                </div>
            </div>
            
            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-300 mb-3">모임 제목</label>
                <input type="text" name="title" class="surface w-full p-3 rounded-lg border border-white/10 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" placeholder="예: 오늘 저녁 같이 드실 분!" required>
            </div>

            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-300 mb-3">상세 내용 (선택)</label>
                <textarea name="description" rows="3" class="surface w-full p-3 rounded-lg border border-white/10 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition" placeholder="모임에 대한 자세한 설명을 적어주세요."></textarea>
            </div>
            
            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-300 mb-3">모임 장소 선택</label>
                <div id="map" style="width:100%;height:300px;" class="rounded-lg bg-gray-800 border border-white/10"></div>
                <input type="hidden" id="lat" name="lat" required>
                <input type="hidden" id="lng" name="lng" required>
                <input type="hidden" id="place_name" name="place_name">
                <div id="clickLatlng" class="text-sm text-gray-400 mt-2">지도를 클릭하여 장소를 선택하세요. (필수)</div>
            </div>

            <div class="mb-8">
                <label class="block text-sm font-medium text-gray-300 mb-3">모임 일정 선택</label>
                <input id="schedule-picker" name="schedule" class="surface w-full p-3 rounded-lg border border-white/10" placeholder="날짜와 시간을 선택하세요..." required>
            </div>

            <button type="submit" class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 rounded-xl text-white font-bold text-lg btn-glow">
                모임 개설하기
            </button>
        </form>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://npmcdn.com/flatpickr/dist/l10n/ko.js"></script>
<script type="text/javascript" src="https://dapi.kakao.com/v2/maps/sdk.js?appkey={{ kakao_map_api_key }}&libraries=services"></script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        flatpickr("#schedule-picker", {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            minDate: "today",
            locale: "ko",
        });

        if ("{{ kakao_map_api_key }}") {
            if (typeof kakao === 'undefined' || !kakao.maps || !kakao.maps.services) {
                document.getElementById('map').innerHTML = '<div class="w-full h-full flex flex-col items-center justify-center text-gray-400 p-4 text-center"><span class="text-3xl mb-2">🗺️</span><p class="font-bold">카카오맵 스크립트를 불러오지 못했습니다.</p></div>';
                return;
            }
            try {
                var mapContainer = document.getElementById('map'),
                    mapOption = { center: new kakao.maps.LatLng(37.566826, 126.9786567), level: 5 };
                var map = new kakao.maps.Map(mapContainer, mapOption);
                var geocoder = new kakao.maps.services.Geocoder();
                var marker = new kakao.maps.Marker({ position: map.getCenter(), map: map });

                kakao.maps.event.addListener(map, 'click', function(mouseEvent) {        
                    var latlng = mouseEvent.latLng; 
                    marker.setPosition(latlng);
                    document.getElementById('lat').value = latlng.getLat();
                    document.getElementById('lng').value = latlng.getLng();
                    searchDetailAddrFromCoords(latlng, function(result, status) {
                        if (status === kakao.maps.services.Status.OK) {
                            var detailAddr = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
                            document.getElementById('clickLatlng').innerText = '선택된 위치: ' + detailAddr;
                            document.getElementById('place_name').value = detailAddr;
                        } else {
                            document.getElementById('clickLatlng').innerText = '선택된 위치의 주소를 가져올 수 없습니다.';
                            document.getElementById('place_name').value = "알 수 없는 위치";
                        }
                    });
                });
                function searchDetailAddrFromCoords(coords, callback) {
                    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
                }
            } catch(e) {
                console.error(e);
                document.getElementById('map').innerHTML = '<div class="w-full h-full flex items-center justify-center text-red-400">지도 초기화 중 오류가 발생했습니다.</div>';
            }
        } else {
            document.getElementById('map').innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-500">Kakao Map API 키가 설정되지 않았습니다. (.env 확인)</div>';
        }
    });
</script>
{% endblock %}
```

---

## **커밋 + PR**

```bash
# 커밋 1: 뷰 로직
git add meetu/backend/meetings/
git commit -m "feat: 모임 목록 조회/필터링, 카카오맵 장소 선택, 타임피커 구현 (#23, #24, #25)"

# 커밋 2: 템플릿
git add meetu/backend/templates/meetings/
git commit -m "feat: 모임 목록/생성 페이지 프론트엔드 구현"

git push -u origin feat/meeting-list-map-schedule
```

**GitHub에서**:
1. "Compare & pull request" 버튼 클릭
2. ⚠️ Base branch를 **develop**으로 설정 (main 아님!)
3. 제목: `feat: PR#1 모임 목록 조회 + 카카오맵 + 타임피커`
4. 리뷰어(Reviewers) 지정 및 리뷰 요청


---

## **🤝 팀원 제공 일정 (인터페이스 계약)**

| 제공 시점 | 산출물 | 수신자 | 용도 |
| --- | --- | --- | --- |
| **PR 머지 직후** | 모임 목록 페이지 (`meeting_list.html`) + "참여하기" 버튼 URL | 임태규 | 참여하기 버튼에 `meeting_join` 뷰 연결 |
| **PR 머지 직후** | 모임 생성 뷰의 위치/일정 저장 로직 | 임태규 | 채팅방 헤더에 장소/일정 표시 |
