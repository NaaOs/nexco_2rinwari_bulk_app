"""2輪割の一括申し込み（申請・承認）を行うモジュールです。"""

from collections.abc import Sequence
from datetime import date

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .constants import ALREADY_APPLIED_MESSAGE, COURSE_ID, DISCOUNT_ORDER_URL, PAGE_ID
from .exceptions import PageStructureError
from .holidays import format_date
from .models import AccountInfo

# 申請内容（割引区分など）を表す固定パラメータです。サイトの入力フォームに合わせています。
_DISCOUNT_CONDITIONS = [["5"], ["1"], ["11"], ["1"]]
_DISCOUNT_CONDITIONS_JSON = '[["5"],["1"],["11"],["1"]]'


def apply_for_discount(
    session: requests.Session, account_info: AccountInfo, dates: Sequence[date]
) -> None:
    """指定した日付それぞれについて、2輪割の申請から承認までを行います。

    既に申し込み済みの日付は読み飛ばします。

    Args:
        session: ログイン済みのリクエストセッション。
        account_info: 申請に使用するETCカード・車載器の登録情報。
        dates: 申し込み対象日の一覧。

    Raises:
        requests.HTTPError: 承認リクエストがHTTPエラーを返した場合。
        PageStructureError: 申請レスポンスから受付番号を取得できなかった場合。
    """
    for target_date in dates:
        date_text = format_date(target_date)

        order_res = session.post(
            DISCOUNT_ORDER_URL, data=_build_order_payload(account_info, date_text)
        )

        if ALREADY_APPLIED_MESSAGE in order_res.text:
            print(f"{date_text}はすでに申し込み済みです")
            continue

        accept_number = _read_accept_number(order_res.text, date_text)
        print(f"{date_text}分を申し込んでいます")

        confirm_res = session.post(
            DISCOUNT_ORDER_URL,
            data=_build_confirmation_payload(account_info, date_text, accept_number),
        )
        confirm_res.raise_for_status()


def _build_order_payload(account_info: AccountInfo, date_text: str) -> dict[str, str]:
    """STEP1（申請）リクエストのフォームデータを組み立てます。"""
    return {
        "id": PAGE_ID,
        "step": "1",
        "date": date_text,
        "er": _DISCOUNT_CONDITIONS_JSON,
        "course": COURSE_ID,
        "price": "s",
        "etc": account_info.etc_number,
        "etc_number": account_info.etc_number,
        "etc_month": account_info.etc_month,
        "etc_year": account_info.etc_year,
        "onboard_number": account_info.onboard_number,
        "free_input": "",
    }


def _build_confirmation_payload(
    account_info: AccountInfo, date_text: str, accept_number: str
) -> dict[str, object]:
    """STEP2（承認）リクエストのフォームデータを組み立てます。"""
    return {
        "id": PAGE_ID,
        "step": "2",
        "course": COURSE_ID,
        "date": date_text,
        "price": "s",
        "etc_number": account_info.etc_number,
        "etc_month": account_info.etc_month,
        "etc_year": account_info.etc_year,
        "accept_number": accept_number,
        "er": _DISCOUNT_CONDITIONS,
        "onboard_number": account_info.onboard_number,
        "number_plate_upside": "",
        "number_plate_downside": "",
        "free_input": "",
    }


def _read_accept_number(response_html: str, date_text: str) -> str:
    """申請レスポンスのHTMLから、承認に必要な受付番号を読み取ります。

    Args:
        response_html: STEP1（申請）リクエストのレスポンスHTML。
        date_text: 対象日付（エラーメッセージ用）。

    Returns:
        受付番号。

    Raises:
        PageStructureError: 受付番号の隠しinput要素が見つからなかった場合。
    """
    soup = BeautifulSoup(response_html, "html.parser")
    field = soup.find("input", attrs={"name": "accept_number", "type": "hidden"})
    if not isinstance(field, Tag) or "value" not in field.attrs:
        raise PageStructureError(f"{date_text}の申請で受付番号を取得できませんでした。")

    return str(field["value"])
