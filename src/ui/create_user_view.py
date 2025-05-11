from tkinter import ttk, StringVar, constants
from services.dayplan_service import DayplanService, UsernameExistsError


class CreateUserView:
    def __init__(self, root, handle_create_user, handle_show_login_view):
        self._root = root
        self._handle_create_user = handle_create_user
        self._handle_show_login_view = handle_show_login_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _create_user_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if len(username) == 0 or len(password) == 0:
            self._show_error("Username and password are required")
            return

        try:
            dayplan_service = DayplanService()
            dayplan_service.create_user(username, password)
            self._handle_create_user()
        except UsernameExistsError:
            self._show_error(f"Username {username} already exists")

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_username_field(self):
        username_label = ttk.Label(master=self._frame, text="Username:")
        self._username_entry = ttk.Entry(master=self._frame)
        username_label.grid(row=1, column=0, padx=5, pady=5, sticky=constants.W)
        self._username_entry.grid(row=1, column=1, padx=5, pady=5, sticky=constants.EW)

    def _initialize_password_field(self):
        password_label = ttk.Label(master=self._frame, text="Password:")
        self._password_entry = ttk.Entry(master=self._frame, show="*")
        password_label.grid(row=2, column=0, padx=5, pady=5, sticky=constants.W)
        self._password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, padding=20)
        self._frame.grid_columnconfigure(0, weight=1, minsize=120)
        self._frame.grid_columnconfigure(1, weight=2, minsize=200)

        title_label = ttk.Label(
            master=self._frame,
            text="Create New Account",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(row=3, column=0, columnspan=2, pady=(0, 5))

        self._initialize_username_field()
        self._initialize_password_field()

        create_user_button = ttk.Button(
            master=self._frame,
            text="Create Account",
            command=self._create_user_handler,
            width=18
        )
        login_button = ttk.Button(
            master=self._frame,
            text="Back to Login",
            command=self._handle_show_login_view,
            width=18 
        )

        create_user_button.grid(row=4, column=0, columnspan=2, padx=5, pady=(15, 5), sticky=constants.N)
        login_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky=constants.N)

        self._hide_error()
