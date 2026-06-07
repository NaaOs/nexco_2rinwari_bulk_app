"""アプリ内で受け渡しするデータ構造を定義します。"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccountInfo:
    """2輪割の申し込みに必要な、ETCカード・車載器の登録情報です。

    Attributes:
        etc_number: ETCカード番号。
        etc_year: ETCカード有効期限（年）。
        etc_month: ETCカード有効期限（月）。
        onboard_number: 車載器管理番号（メインで登録されている番号）。
            「左-中-右」の形式でハイフン結合済みの文字列です。
    """

    etc_number: str
    etc_year: str
    etc_month: str
    onboard_number: str
