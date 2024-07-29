import ttkbootstrap as ttk


class Login(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=0)

        self.loginFrame = ttk.Frame(self)

        ttk.Label(self.loginFrame, text="Логин").pack()
        self.login_entry = ttk.Entry(self.loginFrame)
        self.login_entry.pack(padx=10, pady=(0, 10))

        ttk.Label(self.loginFrame, text="Пароль").pack()
        self.password_entry = ttk.Entry(self.loginFrame, show="*")
        self.password_entry.pack(padx=10, pady=(0, 0))

        self.fail_massage = ttk.Label(
            self.loginFrame, text="", font=("TkDefaultFont", 10)
        )
        self.fail_massage.pack(pady=(5, 0))

        self.loginFrame.pack()

        self.submit_button = ttk.Button(self, text="ОК")
        self.submit_button.pack(expand=True)

    def on_login(self, func):
        self.login_entry.bind("<Return>", func)
        self.password_entry.bind("<Return>", func)
        self.submit_button.bind("<Button-1>", func)

    def get_login(self):
        return self.login_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def set_faild_massage(self, fail_massage):
        self.fail_massage.configure(text=fail_massage)

    def set_login_password(self, login: str, password: str):
        self.login_entry.insert(0, login)
        self.password_entry.insert(0, password)

    def set_focus(self):
        self.login_entry.focus_set()
