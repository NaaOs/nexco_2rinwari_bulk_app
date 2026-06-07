"""ログイン済みアカウントのETCカード・車載器情報を取得するモジュールです。"""

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .constants import MEMBER_EDIT_URL
from .exceptions import PageStructureError
from .models import AccountInfo

# 登録内容変更ページから読み取る、隠しinput要素のname属性です。
_ETC_NUMBER_FIELD = "etc_number_0"
_ETC_YEAR_FIELD = "etc_year_0"
_ETC_MONTH_FIELD = "etc_month_0"
_ONBOARD_NUMBER_FIELDS = ("onboard_left_0", "onboard_middle_0", "onboard_right_0")


def fetch_account_info(session: requests.Session) -> AccountInfo:
    """登録内容変更ページからETCカード・車載器の登録情報を取得します。

    Args:
        session: ログイン済みのリクエストセッション。

    Returns:
        ETCカード番号・有効期限・車載器管理番号を含むアカウント情報。

    Raises:
        requests.HTTPError: ページ取得リクエストがHTTPエラーを返した場合。
        PageStructureError: ページから必要な情報を取得できなかった場合。
            メインで登録されている車載器番号が複数存在する場合もこのエラーになります。
    """
    res = session.get(MEMBER_EDIT_URL)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    onboard_number = "-".join(
        _read_hidden_field(soup, name) for name in _ONBOARD_NUMBER_FIELDS
    )

    return AccountInfo(
        etc_number=_read_hidden_field(soup, _ETC_NUMBER_FIELD),
        etc_year=_read_hidden_field(soup, _ETC_YEAR_FIELD),
        etc_month=_read_hidden_field(soup, _ETC_MONTH_FIELD),
        onboard_number=onboard_number,
    )


def _read_hidden_field(soup: BeautifulSoup, field_name: str) -> str:
    """隠しinput要素からvalue属性の値を読み取ります。

    Args:
        soup: 解析対象ページのパース済みHTML。
        field_name: 読み取る隠しinput要素のname属性値。

    Returns:
        隠しinput要素のvalue属性値。

    Raises:
        PageStructureError: 該当する要素、またはvalue属性が存在しない場合。
    """
    field = soup.find("input", attrs={"name": field_name, "type": "hidden"})
    if not isinstance(field, Tag) or "value" not in field.attrs:
        raise PageStructureError(
            f"登録内容変更ページに '{field_name}' が見つかりませんでした。"
        )

    return str(field["value"])
