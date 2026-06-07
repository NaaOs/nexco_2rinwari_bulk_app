"""2輪割の申し込み対象となる休日（土日・祝日）の一覧を算出するモジュールです。"""

from collections.abc import Iterator
from datetime import date, datetime, timedelta

import jpholiday  # type: ignore[import-untyped]
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .constants import APPLICATION_DETAIL_URL, COURSE_ID
from .exceptions import NoApplicableDateError, PageStructureError

_ONE_DAY: timedelta = timedelta(days=1)


def list_application_dates(session: requests.Session) -> list[date]:
    """申し込み開始日から申し込み最終日までの、休日（土日・祝日）の一覧を取得します。

    申し込み開始日は「年度開始日（4月1日）」と「本日」のうち遅い方です。

    Args:
        session: ログイン済みのリクエストセッション。

    Returns:
        申し込み対象となる休日の一覧（日付の昇順）。

    Raises:
        requests.HTTPError: 申し込み可能日一覧ページの取得に失敗した場合。
        NoApplicableDateError: 申し込み可能な日付が一件も存在しない場合。
        PageStructureError: ページから申し込み最終日を読み取れなかった場合。
    """
    today = datetime.today().date()
    fiscal_year_start = date(today.year, 4, 1)
    start_date = today if today > fiscal_year_start else fiscal_year_start
    end_date = get_last_application_date(session)

    return [
        target_date
        for target_date in _iter_dates(start_date, end_date)
        if _is_holiday(target_date)
    ]


def get_last_application_date(session: requests.Session) -> date:
    """プログラム実行時点における、申し込み可能な最終日を取得します。

    Args:
        session: ログイン済みのリクエストセッション。

    Returns:
        申し込み可能な最終日。

    Raises:
        requests.HTTPError: 申し込み可能日一覧ページの取得に失敗した場合。
        NoApplicableDateError: 申し込み可能な日付が一件も存在しない場合。
        PageStructureError: ページから申し込み最終日を読み取れなかった場合。
    """
    res = session.get(APPLICATION_DETAIL_URL)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    available_cells = soup.find_all("td", class_="available")

    # 1日単位（割引内容が「1日間」）で申請するため、対象コースのセルのみ抽出する。
    # セルのid属性は "{COURSE_ID}_YYYY_MM_DD" の形式。
    course_cell_ids = [
        str(cell.attrs["id"])
        for cell in available_cells
        if isinstance(cell, Tag) and str(cell.attrs.get("id", "")).startswith(COURSE_ID)
    ]

    if not course_cell_ids:
        raise NoApplicableDateError("申し込める日付がありませんでした。")

    last_day_text = course_cell_ids[-1][len(COURSE_ID) + 1 :].replace("_", "/")
    try:
        return datetime.strptime(last_day_text, "%Y/%m/%d").date()
    except ValueError as exc:
        raise PageStructureError(
            f"申し込み最終日の形式を解釈できませんでした: '{last_day_text}'"
        ) from exc


def format_date(target_date: date) -> str:
    """日付を、申し込みフォームが要求する「ゼロ埋めなしのYYYY/M/D」形式の文字列に変換します。

    Args:
        target_date: 変換対象の日付。

    Returns:
        例: 2026年4月7日 -> "2026/4/7"
    """
    return f"{target_date.year}/{target_date.month}/{target_date.day}"


def _is_holiday(target_date: date) -> bool:
    """対象の日付が土日または祝日かどうかを判定します。"""
    return target_date.weekday() >= 5 or jpholiday.is_holiday(target_date)


def _iter_dates(start: date, end: date) -> Iterator[date]:
    """startからendまでの日付を1日刻みで列挙します（両端を含む）。"""
    current = start
    while current <= end:
        yield current
        current += _ONE_DAY
