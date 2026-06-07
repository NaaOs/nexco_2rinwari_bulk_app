"""アプリのメインウィンドウ（ログイン画面）を提供するモジュールです。"""

import tkinter as tk
import webbrowser
from tkinter import messagebox

import requests

from . import auth, discount, holidays, user_info
from .constants import HAYATABI_LINK_URL, LOGIN_SUCCESS_MESSAGE
from .exceptions import HayatabiError, LoginFailedError, NoApplicableDateError

_WINDOW_TITLE = "【ETC二輪車限定】2026二輪車定率割引 一括申込"
_WINDOW_WIDTH = 350
_WINDOW_HEIGHT = 200
_WINDOW_CENTER_OFFSET = 150
_ICON_PATH = "assets/img_link_logo.ico"

_LEFT_MARGIN = 30
_ENTRY_WIDTH = 45


class HayatabiWindow:
    """早旅アカウントでログインし、2輪割の一括申し込みを行うGUIウィンドウです。"""

    def __init__(self) -> None:
        """ウィンドウを構築し、イベントループを開始します。"""
        self._window = tk.Tk()
        self._mail_entry: tk.Entry
        self._password_entry: tk.Entry
        self._build_widgets()
        self._window.mainloop()

    def _build_widgets(self) -> None:
        """ウィンドウ上の各ウィジェットを配置します。"""
        window = self._window
        window.title(_WINDOW_TITLE)
        window.geometry(self._centered_geometry())
        window.iconbitmap(default=_ICON_PATH)

        y = 10
        tk.Label(
            window, text="NEXCO中日本のサイトのアカウントを入力してください"
        ).place(x=_LEFT_MARGIN, y=y)
        y += 20

        link_label = tk.Label(window, text=HAYATABI_LINK_URL, fg="blue", cursor="hand2")
        link_label.place(x=_LEFT_MARGIN, y=y)
        link_label.bind(
            "<Button-1>", lambda _event: webbrowser.open_new(HAYATABI_LINK_URL)
        )
        y += 20

        tk.Label(
            window, text="申し込み時点で申し込める最終日まで自動で申し込めます"
        ).place(x=_LEFT_MARGIN, y=y)
        y += 20

        tk.Label(window, text="メールアドレス").place(x=_LEFT_MARGIN, y=y)
        y += 20
        self._mail_entry = tk.Entry(window, width=_ENTRY_WIDTH)
        self._mail_entry.place(x=_LEFT_MARGIN, y=y)
        y += 30

        tk.Label(window, text="パスワード").place(x=_LEFT_MARGIN, y=y)
        y += 20
        self._password_entry = tk.Entry(window, width=_ENTRY_WIDTH, show="●")
        self._password_entry.place(x=_LEFT_MARGIN, y=y)
        y += 25

        tk.Button(window, text="ログイン", command=self._on_login_clicked).place(
            x=255, y=y
        )

    def _centered_geometry(self) -> str:
        """画面中央付近にウィンドウを配置するための、tkinter geometry文字列を生成します。"""
        x = self._window.winfo_screenwidth() // 2 - _WINDOW_CENTER_OFFSET
        y = self._window.winfo_screenheight() // 2 - _WINDOW_CENTER_OFFSET
        return f"{_WINDOW_WIDTH}x{_WINDOW_HEIGHT}+{x}+{y}"

    def _on_login_clicked(self) -> None:
        """「ログイン」ボタン押下時に、ログインから2輪割の一括申し込みまでを実行します。"""
        mail_address = self._mail_entry.get()
        password = self._password_entry.get()

        try:
            session = auth.login(mail_address, password)
            target_dates = holidays.list_application_dates(session)
            account_info = user_info.fetch_account_info(session)
        except LoginFailedError as exc:
            messagebox.showinfo(title="ログイン結果", message=str(exc))
            return
        except NoApplicableDateError as exc:
            messagebox.showinfo(title="申し込み結果", message=str(exc))
            return
        except (requests.HTTPError, HayatabiError) as exc:
            messagebox.showerror(title="通信エラー", message=str(exc))
            return

        messagebox.showinfo(title="ログイン結果", message=LOGIN_SUCCESS_MESSAGE)

        try:
            discount.apply_for_discount(session, account_info, target_dates)
        except (requests.HTTPError, HayatabiError) as exc:
            messagebox.showerror(title="申し込み結果", message=str(exc))
            return

        last_date_text = holidays.format_date(target_dates[-1])
        messagebox.showinfo(
            title="申し込み結果",
            message=f"{last_date_text}までの申し込みが完了しました",
        )
        print("申し込み完了しました。")
