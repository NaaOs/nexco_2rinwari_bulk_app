import requests
import tkinter as tk

class DoLogin:

    # 早旅トップページ
    HAYATABI_TOP_PAGE = "https://hayatabi.c-nexco.co.jp"

    def doLogin(self, mail_address, passwd):
        # ------------------------------------------------------------------
        # 初期設定
        # ------------------------------------------------------------------

        # ログインするためのオブジェクト
        login_info = {
            "mail": mail_address,
            "passwd": passwd,
            "current_url": self.HAYATABI_TOP_PAGE,
            "step": 2,
            "action": "lgin"
        }

        # ------------------------------------------------------------------
        # ログイン処理
        # ------------------------------------------------------------------

        # セッションを開始
        session = requests.session()

        # ログインする際のURL
        login_url = self.HAYATABI_TOP_PAGE + "/mypage/"

        # ログイン実行
        res = session.post(login_url, data=login_info)

        # ログインが失敗した際の文言があるか確認
        cannot_login = res.text.find("メールアドレスまたはパスワードが一致しません。")

        # もしログイン処理が失敗していたら
        if cannot_login != -1:
            # print("メールアドレスまたはパスワードが一致しません。")
            tk.messagebox.showinfo(title="ログイン結果", message=str("メールアドレスまたはパスワードが一致しません。"))
            

        # エラーならここで例外を発生させる
        res.raise_for_status()

        return session