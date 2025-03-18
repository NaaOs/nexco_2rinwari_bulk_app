import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class GetUserInfo:

    # 早旅トップページ
    HAYATABI_TOP_PAGE = "https://hayatabi.c-nexco.co.jp"

    def getUserInfo(self, session):

        # ------------------------------------------------------------------
        # マイページ遷移
        # ------------------------------------------------------------------
        # htmlにパースする
        mypage_soup = BeautifulSoup(res.text,"html.parser")

        mypage = mypage_soup.select_one(".btns a")

        # マイページのリンクが取得できたかの確認
        if mypage is None:
            return {"message": "マイページが取得できませんでした。開発者にお問い合わせください。"}

        # ログインする際のURL
        login_url = self.HAYATABI_TOP_PAGE + "/mypage/"

        # マイページのURLを取得
        url_mypage = urljoin(login_url, mypage.attrs["href"])

        # マイページに遷移する
        res = session.get(url_mypage)
        # エラーならここで例外を発生させる
        res.raise_for_status()

        # ------------------------------------------------------------------
        # 登録内容変更ページに遷移する
        # ------------------------------------------------------------------

        # 登録内容変更ページURL
        url_editmyinfo = self.HAYATABI_TOP_PAGE + "/mypage/member_edit.html?action=edit&=1709739623657"

        # 登録内容変更ページに遷移する
        res = session.get(url_editmyinfo)
        # エラーならここで例外を発生させる
        res.raise_for_status()

        # ------------------------------------------------------------------
        # 登録内容の取得
        # ・ETCカード番号
        # ・ETCカード有効期限
        # ・車載器管理番号（メインで登録されている番号のみ）
        # ------------------------------------------------------------------

        # htmlにパースする
        edit_soup = BeautifulSoup(res.text,"html.parser")

        # ETC番号を取得
        etc_num = edit_soup.find('input', attrs={"name": 'etc_number_0', "type": 'hidden'})['value']
        # ETC有効期限（年）を取得
        etc_year = edit_soup.find('input', attrs={"name": 'etc_year_0', "type": 'hidden'})['value']
        # ETC有効期限（月）を取得
        etc_month = edit_soup.find('input', attrs={"name": 'etc_month_0', "type": 'hidden'})['value']
        # 車載器管理番号（メインで登録されている番号のみ）を取得
        # 複数あった場合バグる
        onboard_number_left = edit_soup.find('input', attrs={"name":'onboard_left_0', "type": 'hidden'})['value']
        onboard_number_middle = edit_soup.find('input', attrs={"name": 'onboard_middle_0', "type": 'hidden'})['value']
        onboard_number_right = edit_soup.find('input', attrs={"name": 'onboard_right_0', "type": 'hidden'})['value']
        # 車載器管理番号をすべて結合する
        onboard_number = str(onboard_number_left)+"-"+str(onboard_number_middle)+"-"+str(onboard_number_right)

        # ------------------------------------------------------------------
        # アカウント情報出力
        # ------------------------------------------------------------------

        # アカウントの情報が詰まったデータをJSON形式で吐き出す
        account_info_obj = {
            "etc_num": etc_num,
            "etc_year": etc_year,
            "etc_month": etc_month,
            "onboard": onboard_number,
            "message": "ログインに成功しました。\n2輪割を申し込みます。\n申し込みには時間がかかります。\nしばらくお待ちください。"
        }

        return account_info_obj