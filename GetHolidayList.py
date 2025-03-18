from datetime import datetime, date, timedelta
import jpholiday
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.messagebox

class GetHolidayList:

    # 早旅トップページ
    HAYATABI_TOP_PAGE = "https://hayatabi.c-nexco.co.jp"

    # プログラム実行時点の申し込み最終日を取得する
    def get_last_day_of_application(self, session):

        # 申し込み日付を指定する画面の情報を取得
        detail_html = session.get(self.HAYATABI_TOP_PAGE + "/drive/detail.html?id=164&=1711452392647")
        detail_html_soup = BeautifulSoup(detail_html.text,"html.parser")
        # 申し込み可能日を取得
        available_days_list = detail_html_soup.find_all("td", class_="available")

        # 1日単位で申し込むため割引内容が「1日間」で申請するためのIDを抽出
        available_days_list_attrs = [id for id in available_days_list if id.attrs['id'].startswith("5431")]

        # 申し込める日付がなかった場合、メッセージを出してアプリを終了する。
        if len(available_days_list_attrs) == 0:
            tk.messagebox.showinfo(title="申し込み結果", message="申し込める日付がありませんでした。")
            exit()

        # 申し込み可能日の最終日を取得
        last_day = str(available_days_list_attrs[-1].attrs['id'])[5:].replace("_", "/")

        return datetime.strptime(last_day, '%Y/%m/%d').date()

    # 日付フォーマットを確認する関数
    def check_date_format(self, date_input):
        # try-except文でエラーが発生するかどうかをチェック
        try:
            datetime.strptime(date_input, '%Y/%m/%d')
        # 変換に成功したらTrueを返す
            return True
        except ValueError: # 変換に失敗したらFalseを返す
            return False

    # 休日かどうかを判断する関数
    def is_holiday(self, date):
        date = datetime.strptime(date, '%Y/%m/%d')
        # jpholidayのライブラリを使用して祝日判定を行う
        if(date.weekday() >= 5 or jpholiday.is_holiday(date)):
            return True
        else:
            return False

    # 休日の範囲
    def date_range(self, start, stop, step = timedelta(1)):
        current = start
        while current <= stop:
            yield current
            current += step

    def get_holiday(self, session):

        # 休日を格納するリスト
        holiday_list = []
        # 年度の開始から
        start_date = date(datetime.today().year,4,1)

        # 申し込む日が4月１日以降だったら
        if datetime.today().date() > date(datetime.today().year,4,1):
            start_date = datetime.today().date()
            print(f"申し込み開始日は{start_date}です")

        # 申し込み最終日
        end_date = self.get_last_day_of_application(session)

        # 申し込んだ日から年度末までの日付を格納する
        for dy in self.date_range(start_date, end_date):
            dy = str(dy).replace('-', '/')
            # 日付formatをチェックしています
            if(self.check_date_format(dy)):
                # 休日かどうかを判定しています
                if(self.is_holiday(dy)):

                    dy = datetime.strptime(dy, "%Y/%m/%d")
                    # 休日リストに格納する
                    holiday_list.append(dy.strftime("%Y/%#m/%#d"))

                else:
                    continue
            else:
                continue

        return holiday_list