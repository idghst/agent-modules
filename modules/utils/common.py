"""
공통 유틸리티 함수 모듈

이 모듈은 프로젝트 전반에서 사용되는 유틸리티 함수를 제공합니다.
"""

import os
import logging
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def get_project_root() -> Path:
    """
    프로젝트 루트 디렉토리를 반환합니다.

    우선순위:
    1. 환경변수 PROJECT_ROOT
    2. 현재 작업 디렉토리 (os.getcwd())

    Returns:
        프로젝트 루트 경로
    """
    env_root = os.getenv("PROJECT_ROOT")
    if env_root:
        return Path(env_root)

    return Path.cwd()


def load_env(env_file: Optional[str] = None) -> None:
    """
    환경 변수를 로드합니다.

    Args:
        env_file: .env 파일 경로 (기본값: 프로젝트 루트의 .env)
    """
    if env_file is None:
        env_file = get_project_root() / ".env"

    load_dotenv(env_file)


def setup_logging(
    level: Optional[str] = None, format_string: Optional[str] = None
) -> logging.Logger:
    """
    로깅을 설정하고 로거를 반환합니다.

    Args:
        level: 로그 레벨 (기본값: INFO 또는 환경변수 LOG_LEVEL)
        format_string: 로그 포맷 문자열

    Returns:
        설정된 로거 인스턴스
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")

    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=getattr(logging, level.upper()), format=format_string)

    return logging.getLogger(__name__)


def ensure_dir(path: Path) -> Path:
    """
    디렉토리가 존재하지 않으면 생성합니다.

    Args:
        path: 생성할 디렉토리 경로

    Returns:
        생성된 디렉토리 경로
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
