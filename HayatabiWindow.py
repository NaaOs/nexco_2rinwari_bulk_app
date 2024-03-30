import tkinter as tk
import tkinter.messagebox
import GetUserInfo
import GetHolidayList
import webbrowser
import pyautogui as pag
import ApplicationForDiscount

class HayatabiWindow:

    # ユーザー情報を取得する関数です
    def get_user_info(self):
        mail_address = self.mail_box.get()
        passwd = self.passed_box.get()
        # GetHolidayをインスタンス化
        get_holiday = GetHolidayList.GetHolidayList()
        holiday_list = get_holiday.get_holiday(mail_address, passwd)

        # GetUserinfoをインスタンス化
        get_userinfo = GetUserInfo.GetUserInfo()
        result = get_userinfo.getUserInfo(mail_address, passwd)

        if "ログインに成功しました。" in str(result['message']):
            tk.messagebox.showinfo(title="ログイン結果", message=str(result['message']))
            # 取得した情報をもとに2輪割を申し込む
            self.postDiscountForm(result, holiday_list)
            tk.messagebox.showinfo(title="申し込み結果", message=f"{str(holiday_list[-1])}までの申し込みが完了しました")
        else:
            tk.messagebox.showinfo(title="ログイン結果", message=str(result['message']))

    # 2輪割を申し込む関数です
    def postDiscountForm(self, result, holiday_list):
        # 2輪割申し込み
        app_for_discount = ApplicationForDiscount.ApplicationForDiscount()
        app_for_discount.app_for_discount(result, holiday_list)


    # ------------------------------------------------------------------
    # window設定
    # ------------------------------------------------------------------
    def __init__(self):

        # Window変数
        initial_position = 10
        # テキストボックス横幅
        textbox_width = 45

        object_left_position = 30

        window = tk.Tk()
        window.title("【ETC二輪車限定】2024二輪車定率割引 一括申込")
        # Windowサイズ、場所の指定
        window.geometry("350x200+"+str(int(pag.size().width / 2)-150)+"+"+str(int(pag.size().height / 2)-150))
        window.iconbitmap(default='assets/img_link_logo.ico')

        self.website_label = tk.Label(text="NEXCO中日本のサイトのアカウントを入力してください")
        self.website_label.place(x=object_left_position, y=initial_position)
        initial_position+=20

        # 「早旅」のサイトリンクラベル
        self.websitelink_label = tk.Label(text="https://hayatabi.c-nexco.co.jp/?&=1699541541096", fg="blue", cursor="hand2")
        self.websitelink_label.pack()
        self.websitelink_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://hayatabi.c-nexco.co.jp/?&=1699541541096"))
        self.websitelink_label.place(x=object_left_position, y=initial_position)
        initial_position+=20

        self.website_label = tk.Label(text="申し込み時点で申し込める最終日まで自動で申し込めます")
        self.website_label.place(x=object_left_position, y=initial_position)
        initial_position+=20

        # メールアドレスラベル
        self.mail_label = tk.Label(text="メールアドレス")
        self.mail_label.place(x=object_left_position, y=initial_position)
        initial_position+=20

        # メールアドレステキストボックス
        self.mail_box = tk.Entry(width=textbox_width)
        self.mail_box.place(x=object_left_position, y=initial_position)
        initial_position+=30

        # パスワードラベル
        self.passwd_label = tk.Label(text="パスワード")
        self.passwd_label.place(x=object_left_position, y=initial_position)
        initial_position+=20

        # パスワードテキストボックス
        self.passed_box = tk.Entry(width=textbox_width, show="●")
        self.passed_box.place(x=object_left_position, y=initial_position)
        initial_position+=25

        self.button = tk.Button(window, text="ログイン", command=self.get_user_info).place(x=255, y=initial_position)

        window.mainloop()

HayatabiWindow()