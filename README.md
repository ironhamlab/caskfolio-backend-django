# Caskfolio Backend

> 위스키 추천 및 테이스팅 노트 관리 서비스

2026년 버킷리스트 중 하나인 '매달 새로운 술 마셔보기'를 위해 시작한 프로젝트입니다.
위스키를 주제로, AI 기반 추천과 테이스팅 노트를 기록할 수 있는 웹 서비스의 백엔드 API 서버입니다.

<br/>

## 프로젝트 소개

- **서비스명**: Caskfolio
- **AI 챗봇명**: 위스큐레이터(Whiscurator)
- **기술 스택**: Django REST Framework, OpenAI API, LangChain

<br/>

## 주요 기능

### 1. 인증 및 사용자 관리
- JWT 기반 인증 (access token + refresh token)
- 소셜 로그인 (Google, Kakao)
- 커스텀 User 모델 (소프트 삭제 지원)

### 2. 위스키 데이터베이스
- 위스키 정보 관리 (증류소, 국가, 지역, 타입, 피트 레벨 등)
- 플레이버 프로필, 서빙 가이드, 페어링 정보
- 캐스크 타입 다대다 관계

### 3. 테이스팅 노트
- 개인 위스키 테이스팅 기록 작성/조회/수정/삭제
- 공개/비공개 설정
- 별점, 태그, 노즈/팔레트/피니시 노트
- 필터링 및 검색 기능

### 4. 컬렉션
- 소유한 위스키 관리 ("위스키 장식장")
- 구매 날짜, 가격, 메모 기록

### 5. AI 위스키 큐레이터
- OpenAI GPT-4o-mini 기반 챗봇
  - 위스키 DB 컨텍스트 제공
  - 사용자 취향 데이터 분석 (테이스팅 노트, 컬렉션)
- 개인화된 위스키 추천
- 대화 세션 관리

<br/>

## 기술 스택

### Backend
- **Framework**: Django 6.0, Django REST Framework 3.16
- **Authentication**: dj-rest-auth, django-allauth, djangorestframework-simplejwt
- **Database**: SQLite (개발용)
- **AI/ML**: OpenAI API, LangChain
- **기타**: django-cors-headers, django-filter, Pillow, python-dotenv

### 개발 도구
- **Package Manager**: Poetry
- **Python Version**: 3.14+

<br/>

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/ironhamlab/caskfolio-backend-django.git
cd caskfolio-backend-django
```

### 2. Poetry 설치 (설치되지 않은 경우)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. 의존성 설치
```bash
poetry install
```

### 4. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일 생성
```bash
cp .env.example .env
```

**SECRET_KEY 생성**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

생성된 키를 복사하여 `.env` 파일에 입력:
```env
# Django secret key
SECRET_KEY=django-insecure-abc123xyz...

# Debug mode (개발: True, 배포: False)
DEBUG=True

# OpenAI API key (https://platform.openai.com/api-keys 에서 발급)
OPENAI_API_KEY=sk-your-api-key-here
```

### 5. 데이터베이스 마이그레이션
```bash
poetry run python manage.py migrate
```

### 6. 슈퍼유저 생성 (선택)
```bash
poetry run python manage.py createsuperuser
```

### 7. 개발 서버 실행
```bash
poetry run python manage.py runserver
```


<br/>

## API 엔드포인트

### 인증
- `POST /api/accounts/signup/` - 회원가입
- `POST /api/accounts/login/` - 로그인
- `POST /api/accounts/logout/` - 로그아웃
- `POST /api/accounts/token/refresh/` - 토큰 갱신
- `GET /api/accounts/user/` - 현재 사용자 정보

### 위스키
- `GET /api/whiskies/` - 위스키 목록
- `GET /api/whiskies/{id}/` - 위스키 상세

### 테이스팅 노트
- `GET /api/tasting/notes/` - 공개 노트 피드
- `GET /api/tasting/my-notes/` - 내 노트 목록
- `POST /api/tasting/notes/create/` - 노트 작성
- `GET /api/tasting/notes/{id}/` - 노트 상세
- `PUT /api/tasting/notes/{id}/` - 노트 수정
- `DELETE /api/tasting/notes/{id}/` - 노트 삭제

### 컬렉션
- `GET /api/collection/my-collection/` - 내 컬렉션
- `POST /api/collection/add/` - 위스키 추가
- `DELETE /api/collection/{id}/` - 위스키 제거

### AI 큐레이터
- `GET /api/curator/sessions/` - 대화 세션 목록
- `GET /api/curator/sessions/{id}/` - 세션 상세
- `POST /api/curator/chat/` - 메시지 전송
- `DELETE /api/curator/sessions/{id}/` - 세션 삭제

<br/>

## 프로젝트 구조

```
caskfolio-backend-django/
├── apps/
│   ├── accounts/       # 사용자 인증 및 관리
│   ├── whisky/         # 위스키 데이터베이스
│   ├── tasting/        # 테이스팅 노트
│   ├── collection/     # 위스키 컬렉션
│   └── curator/        # AI 큐레이터 챗봇
├── config/             # Django 설정
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example        # 환경 변수 예시
├── .gitignore
├── manage.py
├── pyproject.toml      # Poetry 의존성 관리
└── README.md
```

<br/>

## 주요 기술적 구현

### 1. AI 위스키 큐레이터
  - OpenAI GPT-4o-mini 기반 챗봇
  - 프롬프트 엔지니어링을 통한 개인화 추천
    - 위스키 DB 컨텍스트 주입
    - 사용자 취향 데이터 분석 (테이스팅 노트, 컬렉션)

### 2. 쿼리 최적화
- `select_related`, `prefetch_related`를 활용한 N+1 쿼리 방지

### 3. 권한 관리
- `IsAuthenticated`, `IsAuthenticatedOrReadOnly` 등 뷰 단위 권한 설정
- 비공개 노트 접근 제어

### 4. 소프트 삭제
- 커스텀 UserManager를 통한 삭제된 사용자 필터링

<br/>

## Git Commit 컨벤션

| 타입 | 설명 |
|------|------|
| feat | 새로운 기능 추가 |
| fix | 버그 수정 |
| docs | 문서 수정 |
| refactor | 코드 리팩토링 |
| style | 코드 포맷팅 (코드 변경 없음) |
| chore | 빌드, 패키지 관리 |

<br/>

## Branch 전략

- `main`: 배포 가능한 상태 관리
- `develop`: feature 브랜치 병합용
- `feature/*`: 기능 개발 및 버그 수정

> MVP는 1인 개발의 편의를 위해 main 브랜치에서 진행

<br/>

## 향후 개발 계획

- [ ] PostgreSQL 전환
- [ ] 위스키 이미지 CDN 연동
- [ ] 테이스팅 노트 통계 및 분석 기능
- [ ] 소셜 기능 (팔로우, 좋아요, 댓글)
- [ ] 위스키 평가 알고리즘 개선
- [ ] API 문서 자동화 (drf-spectacular)
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축

<br/>

## 라이선스

이 프로젝트는 개인 포트폴리오 목적으로 제작되었습니다.


