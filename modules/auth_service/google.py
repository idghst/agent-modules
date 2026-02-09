"""
Google API 인증 모듈

이 모듈은 Google API 인증을 통합 관리합니다.
Calendar와 Gmail API를 함께 사용할 수 있도록 스코프를 통합합니다.
"""

import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from agent_modules.utils import get_project_root


# 통합 스코프 (Calendar 읽기 + Gmail 전송)
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def get_credentials() -> Credentials:
    """
    Google API 자격 증명을 가져옵니다.

    통합된 스코프를 사용하여 Calendar와 Gmail API를
    모두 사용할 수 있는 토큰을 생성/갱신합니다.

    Returns:
        Google API 자격 증명 객체

    Raises:
        FileNotFoundError: credentials.json 파일이 없는 경우
    """
    project_root = get_project_root()
    credentials_path = project_root / os.getenv(
        "GOOGLE_CREDENTIALS_PATH", "credentials.json"
    )
    token_path = project_root / os.getenv("GOOGLE_TOKEN_PATH", "token.json")

    creds = None

    # 기존 토큰 로드
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # 토큰이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"credentials.json 파일을 찾을 수 없습니다: {credentials_path}\n"
                    "Google Cloud Console에서 OAuth 2.0 자격 증명을 다운로드하세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds


def get_calendar_service():
    """
    Google Calendar API 서비스를 반환합니다.

    Returns:
        Calendar API 서비스 객체
    """
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)


def get_gmail_service():
    """
    Gmail API 서비스를 반환합니다.

    Returns:
        Gmail API 서비스 객체
    """
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)
