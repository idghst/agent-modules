"""
Google API 인증 모듈

이 모듈은 Google API 인증을 통합 관리합니다.
Calendar와 Gmail API를 함께 사용할 수 있도록 스코프를 통합합니다.
"""

import os
from pathlib import Path

from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from modules.utils import get_project_root


# 통합 스코프 (Calendar 읽기 + Gmail 전송)
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def get_credentials(
    credentials_path: Optional[str] = None, token_path: Optional[str] = None
) -> Credentials:
    """
    Google API 자격 증명을 가져옵니다.

    Args:
        credentials_path: credentials.json 파일 경로 (선택)
        token_path: token.json 파일 경로 (선택)

    Returns:
        Google API 자격 증명 객체

    Raises:
        FileNotFoundError: credentials.json 파일이 없는 경우
    """
    project_root = get_project_root()

    if not credentials_path:
        credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")

    if not token_path:
        token_path = os.getenv("GOOGLE_TOKEN_PATH", "token.json")

    # 절대 경로가 아니면 프로젝트 루트 기준 상대 경로로 처리
    cred_path_obj = Path(credentials_path)
    if not cred_path_obj.is_absolute():
        cred_path_obj = project_root / credentials_path

    token_path_obj = Path(token_path)
    if not token_path_obj.is_absolute():
        token_path_obj = project_root / token_path

    creds = None

    # 기존 토큰 로드
    if token_path_obj.exists():
        creds = Credentials.from_authorized_user_file(str(token_path_obj), SCOPES)

    # 토큰이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not cred_path_obj.exists():
                raise FileNotFoundError(
                    f"credentials.json 파일을 찾을 수 없습니다: {cred_path_obj}\n"
                    "Google Cloud Console에서 OAuth 2.0 자격 증명을 다운로드하거나 "
                    "GOOGLE_CREDENTIALS_PATH 환경변수를 설정하세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_path_obj), SCOPES)
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        with open(token_path_obj, "w") as token:
            token.write(creds.to_json())

    return creds


def get_calendar_service(
    credentials_path: Optional[str] = None, token_path: Optional[str] = None
):
    """
    Google Calendar API 서비스를 반환합니다.

    Returns:
        Calendar API 서비스 객체
    """
    creds = get_credentials(credentials_path, token_path)
    return build("calendar", "v3", credentials=creds)


def get_gmail_service(
    credentials_path: Optional[str] = None, token_path: Optional[str] = None
):
    """
    Gmail API 서비스를 반환합니다.

    Returns:
        Gmail API 서비스 객체
    """
    creds = get_credentials(credentials_path, token_path)
    return build("gmail", "v1", credentials=creds)
