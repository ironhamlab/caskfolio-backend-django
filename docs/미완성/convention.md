# Caskfolio Development Convention
## 1. 아키텍처 결정사항
### 소프트 딜리트 (Soft Delete)

회원 탈퇴 시 DB에서 즉시 삭제하지 않고 deleted_at 필드에 시각 기록
탈퇴 유저가 작성한 공개 테이스팅 노트 처리 보존 목적
is_active = False 함께 처리

### country 필드 제거

country는 DB 필드로 관리하지 않고 style 필드에서 유추하는 @property로 처리
이유: style과 country 중복 저장 시 데이터 불일치 가능성 차단

```python
@property
def country(self):
    scotch = ["scotch_single_malt", "scotch_blended", "scotch_blended_malt", "scotch_single_grain"]
    if self.style in scotch:
        return "Scotland"
    mapping = {
        "bourbon": "USA", "rye": "USA", "tennessee": "USA",
        "irish": "Ireland",
        "japanese_single_malt": "Japan", "japanese_blended": "Japan",
    }
    return mapping.get(self.style, "Other")
```

## 2. 모델 관련 규칙
### TastingNote

같은 유저가 같은 위스키를 여러 번 기록 가능 (unique_together 없음)
tasted_at : 실제 마신 날짜 (유저 직접 입력, 기본값 오늘)
created_at : 기록 작성 시각 (자동)
두 필드를 분리하는 이유 : 과거 경험 소급 기록 허용

### TastingNote 태그

유저 자유 입력 방식 (인스타그램 태그 형식)
태그당 최대 20자, 최대 10개
유효성 검사는 Serializer 레벨에서 처리
flavor_profile (Whisky 모델 공식 수치) 과 혼용 금지 — 역할 명확히 분리

flavor_profile : 관리자가 입력하는 공식 Radar Chart 데이터
tags : 유저가 자유롭게 입력하는 주관적 테이스팅 표현



### CaskType

Whisky 모델과 ManyToMany 관계
더블캐스크 등 복수 캐스크 표현 가능
새로운 캐스크 타입 추가 시 모델 변경 없이 데이터만 추가


## 3. 비즈니스 로직 규칙
### Collection / Wishlist 자동 처리

위스키를 Collection(장식장)에 추가할 때 동일 위스키가 Wishlist에 있으면 자동 삭제
모델 레벨이 아닌 서비스 로직 레벨에서 처리

```python
def add_to_collection(user, whisky):
    Collection.objects.get_or_create(user=user, whisky=whisky)
    Wishlist.objects.filter(user=user, whisky=whisky).delete()
```

### 테이스팅 노트 공개 여부

개별 노트마다 is_public 부여
앱 설정(note_default_public)은 새 노트 작성 시 기본값으로만 사용
작성 후 개별 변경 가능


## 4. AI (Whiscurator)
### RAG 구조

Whisky 모델의 description, history, bartender_tip, pairing, serving_guide 필드를 벡터 임베딩 소스로 활용
유저 취향 컨텍스트 : 해당 유저의 Collection, TastingNote 별점/태그 데이터를 프롬프트에 포함 (Phase 5)

### 태그 자동 추출 미적용 결정

테이스팅 노트 작성 시 AI 태그 자동 추출 기능은 MVP에서 제외
이유 : Whiscurator에서 이미 OpenAI API 사용, 태그 추출만을 위한 추가 API 호출은 비용 및 복잡도 대비 효용 낮음
대신 유저 자유 입력 태그 방식 채택


## 5. 기타
인증

* JWT 인증 사용

개발 순서 (MVP 기준)

1. User / Auth
2. Whisky / CaskType 모델 + Admin
3. 아카이브 목록, 검색, 필터, 상세 API
4. TastingNote CRUD + Collection / Wishlist
5. 마이페이지 API (내 바, 활동 로그, 여정 시각화)
6. Whiscurator (RAG + ChatSession / ChatMessage)