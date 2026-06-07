"""早旅サイトのURLや年度依存IDなど、アプリ全体で共有する定数を定義します。"""

from typing import Final

# 早旅トップページ
HAYATABI_TOP_PAGE: Final[str] = "https://hayatabi.c-nexco.co.jp"

# トップページへのリンク（GUIに表示するURL）
HAYATABI_LINK_URL: Final[str] = "https://hayatabi.c-nexco.co.jp/?&=1699541541096"

# 年度ごとに変わる、申し込み対象プランのページID
PAGE_ID: Final[str] = "203"

# 年度ごとに変わる、申し込み対象プランのコースID
COURSE_ID: Final[str] = "5661"

# ログインURL
LOGIN_URL: Final[str] = f"{HAYATABI_TOP_PAGE}/mypage/"

# 登録内容変更ページURL（ETCカード情報の取得元）
MEMBER_EDIT_URL: Final[str] = f"{HAYATABI_TOP_PAGE}/mypage/member_edit.html?action=edit"

# 申し込み可能日の一覧が表示される詳細ページURL
APPLICATION_DETAIL_URL: Final[str] = (
    f"{HAYATABI_TOP_PAGE}/drive/detail.html?id={PAGE_ID}&=1746180133958"
)

# 2輪割の申し込み・承認を行うURL
DISCOUNT_ORDER_URL: Final[str] = f"{HAYATABI_TOP_PAGE}/drive/order.html"

# ログイン失敗時に早旅サイトが返す文言
LOGIN_FAILURE_MESSAGE: Final[str] = "メールアドレスまたはパスワードが一致しません。"

# 同一日への重複申し込み時に早旅サイトが返す文言
ALREADY_APPLIED_MESSAGE: Final[str] = (
    "同じ出発日に複数のプランを申込むことはできません。"
)

# ログイン成功時にユーザーへ案内するメッセージ
LOGIN_SUCCESS_MESSAGE: Final[str] = (
    "ログインに成功しました。\n"
    "2輪割を申し込みます。\n"
    "申し込みには時間がかかります。\n"
    "しばらくお待ちください。"
)
