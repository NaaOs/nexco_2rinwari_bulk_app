"""早旅サイトとのやり取りで発生しうる、アプリ固有の例外を定義します。"""


class HayatabiError(Exception):
    """早旅サイトとのやり取りに関するエラーの基底クラスです。"""


class LoginFailedError(HayatabiError):
    """メールアドレスまたはパスワードが一致せず、ログインに失敗した場合に送出します。"""


class NoApplicableDateError(HayatabiError):
    """申し込み可能な日付が一件も存在しない場合に送出します。"""


class PageStructureError(HayatabiError):
    """早旅サイトのレスポンスから期待した要素を取得できなかった場合に送出します。

    サイトのHTML構造が変更された際に発生しうるエラーです。
    """
