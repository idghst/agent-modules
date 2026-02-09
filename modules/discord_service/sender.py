"""
Discord 알림 전송 모듈

Discord Webhook을 사용하여 알림을 전송합니다.
"""

import os
import requests
from typing import Optional


class DiscordSender:
    """Discord Webhook을 사용한 알림 전송 클래스"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        초기화

        Args:
            webhook_url: Discord Webhook URL (기본값: 환경변수 DISCORD_WEBHOOK_URL)
        """
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def send_message(self, content: str) -> bool:
        """
        메시지를 전송합니다.

        Args:
            content: 전송할 메시지 내용

        Returns:
            전송 성공 여부

        Raises:
            ValueError: Webhook URL이 설정되지 않은 경우
        """
        if not self.webhook_url:
            raise ValueError("Discord Webhook URL이 설정되지 않았습니다.")

        payload = {"content": content}

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Discord 메시지 전송 실패: {e}")
            return False
