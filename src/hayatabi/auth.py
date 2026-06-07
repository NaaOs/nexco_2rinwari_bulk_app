"""早旅サイトへのログイン処理を行うモジュールです。"""

import requests

from .constants import HAYATABI_TOP_PAGE, LOGIN_FAILURE_MESSAGE, LOGIN_URL
from .exceptions import LoginFailedError


def login(mail_address: str, passwd: str) -> requests.Session:
    """早旅サイトにログインし、ログイン済みのセッションを返します。

    Args:
        mail_address: ログインに使用するメールアドレス。
        passwd: ログインに使用するパスワード。

    Returns:
        ログイン済みのリクエストセッション。

    Raises:
        LoginFailedError: メールアドレスまたはパスワードが一致しなかった場合。
        requests.HTTPError: ログインリクエストがHTTPエラーを返した場合。
    """
    session = requests.session()

    login_info = {
        "mail": mail_address,
        "passwd": passwd,
        "current_url": HAYATABI_TOP_PAGE,
        "step": 2,
        "action": "lgin",
    }

    res = session.post(LOGIN_URL, data=login_info)
    res.raise_for_status()

    if LOGIN_FAILURE_MESSAGE in res.text:
        raise LoginFailedError(LOGIN_FAILURE_MESSAGE)

    return session
