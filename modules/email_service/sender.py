"""
Gmail API를 사용한 이메일 전송 모듈

이 모듈은 Google Gmail API를 통해 이메일을 전송합니다.
"""

import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List

from agent_modules.auth_service import get_gmail_service


class EmailSender:
    """Gmail API를 사용한 이메일 전송 클래스"""

    def __init__(self):
        self.service = get_gmail_service()

    def send_email(
        self,
        subject: str,
        body: str,
        to: Optional[str] = None,
        html: bool = False,
        cc: Optional[List[str]] = None,
    ) -> dict:
        """
        이메일을 전송합니다.

        Args:
            subject: 이메일 제목
            body: 이메일 본문
            to: 수신자 이메일 (기본값: 환경변수 EMAIL_RECIPIENT)
            html: HTML 형식 여부 (기본값: False)
            cc: 참조 수신자 목록

        Returns:
            전송 결과 (메시지 ID 포함)

        Raises:
            ValueError: 필수 파라미터 누락 시
        """
        # 기본값 설정
        to = to or os.getenv("EMAIL_RECIPIENT")

        if not to:
            raise ValueError("수신자 이메일이 지정되지 않았습니다.")

        # 메시지 생성 (from 헤더 생략 - Gmail API가 인증된 계정을 자동 사용)
        message = MIMEMultipart()
        message["to"] = to
        message["subject"] = subject

        if cc:
            message["cc"] = ", ".join(cc)

        # 본문 추가
        content_type = "html" if html else "plain"
        message.attach(MIMEText(body, content_type))

        # Base64 인코딩
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        # 이메일 전송
        result = (
            self.service.users()
            .messages()
            .send(userId="me", body={"raw": raw_message})
            .execute()
        )

        return result
