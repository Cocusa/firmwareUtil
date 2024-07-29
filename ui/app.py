import logging
import ttkbootstrap as ttk
import tkinter as tk
from services.enviroment_helper import get_user_auth, save_users_auth
from services.logger_configurations import configure_init_log
import technical_control
from technical_control_controller import (
    change_contol_stage,
    get_technical_contol_output,
    get_technical_control_table,
    reset_control_table,
)
from ui.process_output_ui import SerialNumberEntry
from ui.login_ui import Login
from services.ERP_api import AuthException, ERPApi
import traceback
from models.technical_control_model import ControlInfo


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, erpApi):
        super().__init__(parent)
        self.erpApi = erpApi
        self.parent = parent
        self.geometry('250x220')
        self.title('Авторизация')

        self.resizable(False, False)

        self.login_form = Login(self)

        self.login_form.on_login(self.login)
        self.login_form.pack(padx=10, pady=10)

        saved_login, saved_password = get_user_auth()
        self.login_form.set_login_password(saved_login, saved_password)

        self.login_form.set_focus()

        self.protocol("WM_DELETE_WINDOW", self.close_login)

    def close_login(self):
        self.destroy()
        self.parent.destroy()

    def login(self, event):
        try:
            cur_login, cur_password = self.login_form.get_login(), self.login_form.get_password()
            self.erpApi.connect(cur_login, cur_password)
            # login_window.destroy()
            self.withdraw()
            self.parent.deiconify()
            save_users_auth(cur_login, cur_password)
            self.parent.sn_entry.set_focus()
        except AuthException as ex:
            self.login_form.set_faild_massage(str(ex))
            logging.error(str(ex))
        except Exception as ex:
            self.login_form.set_faild_massage("Ошибка подключения")
            logging.error(str(ex) + "\n" + traceback.format_exc())


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__()
        self.erpApi = ERPApi()

        self.title('ВАЦ-ОТК')
        style = self.style
        style.configure(".", font=("TkDefaultFont", 15))
        self.geometry("700x700")
        self.minsize(600, 500)

        main_frame = ttk.Frame(self, padding=5)

        self.sn_entry = SerialNumberEntry(main_frame)
        self.sn_entry.on_enter(self.submit)

        self.current_sn_label = ttk.Label(main_frame, text="Не было произведено проверок.")
        self.table_process = get_technical_control_table(main_frame)
        self.error_output = get_technical_contol_output(main_frame)

        self.sn_entry.pack(side="top")
        self.current_sn_label.pack(side="top")
        self.table_process.pack(fill="x", expand=False, side="top")
        self.error_output.pack(fill="both", expand=True, side="top")

        main_frame.pack(fill="both", expand=True)

        self.init_login()
        self.withdraw()


    def submit(self, event):
        try:
            self.ui_clear()
            serial_number = self.sn_entry.get()
            self.current_sn_label.configure(text=f"Проверка по серийному номеру {serial_number}")
            technical_control.start_technical_control(serial_number, self.ui_react, self.erpApi, self)
            self.sn_entry.set_focus()
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            self.error_output.next("Произошла ошибка:")
            self.error_output.next(str(ex))
            self.error_output.next(traceback.format_exc())
            logging.critical(str(ex) + "\n" + traceback.format_exc())


    def init_login(self):
        LoginWindow(self, self.erpApi)

    def ui_react(self, info: ControlInfo):
        change_contol_stage(self.table_process, self.error_output, info)


    def ui_clear(self):
        self.error_output.clear()
        reset_control_table(self.table_process)            

