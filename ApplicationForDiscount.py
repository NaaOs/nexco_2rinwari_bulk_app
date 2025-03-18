import requests
from bs4 import BeautifulSoup

# 2輪割を申し込むクラスです
class ApplicationForDiscount:

    # 早旅トップページ
    HAYATABI_TOP_PAGE = "https://hayatabi.c-nexco.co.jp"

    # 申し込み承認までをリクエスト
    def sendReq(self, session, user_info, holiday_list):

        # ------------------------------------------------------------------
        # 休日分申請を行う
        # ------------------------------------------------------------------

        for date in holiday_list:

            # 申し込む際のリクエストの中身
            discount_order = {
                "id": "164",
                "step": "1",
                "date": str(date),
                "er": "[[\"5\"],[\"1\"],[\"11\"],[\"1\"]]",
                "course": "5431",
                "price": "s",
                "etc": user_info['etc_num'],
                "etc_number": user_info['etc_num'],
                "etc_month": user_info['etc_month'],
                "etc_year": user_info['etc_year'],
                "onboard_number": user_info['onboard'],
                "free_input": ""
            }

            discount_order_url = self.HAYATABI_TOP_PAGE + "/drive/order.html"

            # # STEP1リクエスト送信
            apped_discount_res = session.post(discount_order_url, data=discount_order)

            # 申し込み済みの場合
            if ("同じ出発日に複数のプランを申込むことはできません。" in apped_discount_res.text):
                print(f"{date}はすでに申し込み済みです")
                continue

            # ------------------------------------------------------------------
            # レスポンスの情報から「accept_number」を取得する
            # ------------------------------------------------------------------

            # htmlにパースする
            apped_discount_soup = BeautifulSoup(apped_discount_res.text,"html.parser")

            print(str(date)+"分を申し込んでいます")
            accept_number = apped_discount_soup.find('input', attrs={"name": 'accept_number', "type": 'hidden'})['value']

            # ------------------------------------------------------------------
            # 得られた情報から申請承認リスクエストを送信
            # ------------------------------------------------------------------

            # 申し込む際のリクエストの中身
            discount_order_step2 = {
                "id": "164",
                "step": "2",
                "course": "5431",
                "date": str(date),
                "price": "s",
                "etc_number": user_info['etc_num'],
                "etc_month": user_info['etc_month'],
                "etc_year": user_info['etc_year'],
                "accept_number": str(accept_number),
                "er": [["5"],["1"],["11"],["1"]],
                "onboard_number": user_info['onboard'],
                "number_plate_upside": "",
                "number_plate_downside": "",
                "free_input": ""
            }

            # STEP2承認
            confirm_screen = session.post(discount_order_url, data=discount_order_step2)
            # エラーならここで例外を発生させる
            confirm_screen.raise_for_status()

    def app_for_discount(self, user_info, holiday_list, login_session):

        # ------------------------------------------------------------------
        # 申し込み処理
        # ------------------------------------------------------------------

        # テスト用（1日だけ実行用）
        # holiday_list = ['2024/4/7']
        # self.sendReq(session, user_info, holiday_list)

        # 本番用
        self.sendReq(login_session, user_info, holiday_list)
