# Agent Google Calendar Modules

이 패키지는 Google Calendar 및 Gmail API와 상호작용하기 위한 에이전트 모듈들을 제공합니다.
다른 프로젝트에서 재사용 가능한 형태로 구성되었습니다.

## 📦 설치 방법

### 로컬 개발 모드 설치
프로젝트 루트에서 다음 명령어를 실행하여 설치합니다:

```bash
pip install -e .
```

### Git URL을 통한 설치
다른 프로젝트의 `requirements.txt`에 다음과 같이 추가하여 사용할 수 있습니다:

```text
git+https://github.com/your-repo/agent-modules.git@main#egg=agent-google-calendar-modules
```

## ⚙️ 설정 및 인증 (필수)

이 모듈을 사용하는 프로젝트(실행 위치)에 다음 설정 파일들이 필요합니다.

### 1. 환경 변수 설정 (.env)
프로젝트 실행 위치에 `.env` 파일을 생성하고 다음 내용을 설정하세요.

```ini
# Google API 인증 파일 경로 (기본값: 실행 위치의 credentials.json, token.json)
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_TOKEN_PATH=token.json

# 이메일 수신자 (선택)
EMAIL_RECIPIENT=your_email@example.com

# 로깅 레벨 (선택, 기본값: INFO)
LOG_LEVEL=INFO
```

### 2. Google API 인증 (credentials.json)
1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성합니다.
2. JSON 파일을 다운로드하여 프로젝트 실행 위치에 `credentials.json`으로 저장합니다.
3. 최초 실행 시 브라우저가 열리며 인증을 진행하고, `token.json`이 자동으로 생성됩니다.

> **주의**: `credentials.json`과 `token.json`, `.env` 파일은 보안상 **절대 Git에 커밋하지 마세요**.

## 🚀 사용 예시

### 이메일 전송

```python
from modules.email_service.sender import EmailSender

sender = EmailSender()
sender.send_email(
    to_email="recipient@example.com",
    subject="테스트 메일",
    body="안녕하세요, 테스트 메일입니다."
)
```

### 캘린더 이벤트 조회

```python
from modules.calendar_service.fetcher import CalendarFetcher

fetcher = CalendarFetcher()
events = fetcher.fetch_events(hours=24)
for event in events:
    print(f"이벤트: {event['summary']} ({event['start']})")
```

## 📂 패키지 구조

- `modules.auth_service`: Google API 인증 처리
- `modules.calendar_service`: 캘린더 이벤트 조회 및 처리
- `modules.email_service`: Gmail을 이용한 메일 전송
- `modules.discord_service`: Discord 알림 전송 (옵션)
- `modules.utils`: 공통 유틸리티

## 📝 라이선스

MIT License