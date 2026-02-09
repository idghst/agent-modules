"""
Google Calendar API 서비스 모듈

이 모듈은 Google Calendar API를 통해 캘린더 이벤트를 조회합니다.
"""

import datetime
from typing import List, Dict

from googleapiclient.errors import HttpError

from agent_modules.auth_service import get_calendar_service


class CalendarFetcher:
    """캘린더 이벤트 조회 클래스"""

    def __init__(self):
        self.service = get_calendar_service()

    def get_upcoming_events(
        self, hours: int = 2, max_results_per_calendar: int = 10
    ) -> List[Dict]:
        """
        모든 캘린더에서 지정된 시간 내의 이벤트를 조회합니다.

        Args:
            hours: 조회할 시간 범위 (기본값: 2시간)
            max_results_per_calendar: 캘린더당 최대 결과 수

        Returns:
            이벤트 목록 (시작 시간 순 정렬)
        """
        # 현재 시간 및 미래 시간 계산 (UTC)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        future = (
            datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
        ).isoformat() + "Z"

        # 모든 캘린더 목록 조회
        calendar_list_result = self.service.calendarList().list().execute()
        calendar_list = calendar_list_result.get("items", [])

        all_events = []

        for calendar_entry in calendar_list:
            calendar_id = calendar_entry["id"]
            calendar_summary = calendar_entry.get("summary", "Unknown Calendar")

            try:
                events_result = (
                    self.service.events()
                    .list(
                        calendarId=calendar_id,
                        timeMin=now,
                        timeMax=future,
                        maxResults=max_results_per_calendar,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                for event in events:
                    # 캘린더 이름 추가
                    event["calendar_summary"] = calendar_summary
                    all_events.append(event)

            except HttpError as e:
                print(f"⚠️ 캘린더 '{calendar_summary}' 조회 실패: {e}")

        # 시작 시간 기준 정렬
        all_events.sort(
            key=lambda x: x["start"].get("dateTime", x["start"].get("date"))
        )

        return all_events

    def format_event_time(self, event: Dict) -> str:
        """
        이벤트 시간을 포맷팅합니다.

        Args:
            event: 이벤트 딕셔너리

        Returns:
            포맷팅된 시간 문자열 (예: "14:00 ~ 15:30")
        """
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        try:
            start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            end_dt = datetime.datetime.fromisoformat(end.replace("Z", "+00:00"))
            return f"{start_dt.strftime('%H:%M')} ~ {end_dt.strftime('%H:%M')}"
        except ValueError:
            return start
