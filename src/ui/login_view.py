from tkinter import ttk, StringVar, constants
from services.dayplan_service import DayplanService, InvalidCredentialsError
from ui.dayplan_view import DayPlanView


class LoginView:

    def __init__(self, root, handle_login, handle_show_create_user_view):

        self._root = root
        self._handle_login = handle_login
        self._handle_show_create_user_view = handle_show_create_user_view
        self._frame = None
        self._username_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None
        self.dayplan_service = DayplanService()

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        try:
            user = self.dayplan_service.login(username, password)
            self._handle_login(user)
        except InvalidCredentialsError:
            self._show_error("Invalid username or password")

    def _show_day_plan_view(self, user):
        self._logged_in_user = user
        self._hide_current_view()

        self._current_view = DayPlanView(
            self._root,
            user,
            self._show_add_plans_view
        )
        self._current_view.pack()

        self.destroy()

    def _show_error(self, message):
        self._error_variable.set(message)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_username_field(self):
        username_label = ttk.Label(master=self._frame, text="Username")
        self._username_entry = ttk.Entry(master=self._frame)

        username_label.grid(padx=5, pady=5, sticky=constants.W)
        self._username_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_password_field(self):
        password_label = ttk.Label(master=self._frame, text="Password")
        self._password_entry = ttk.Entry(master=self._frame)

        password_label.grid(padx=5, pady=5, sticky=constants.W)
        self._password_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.pack(fill=constants.BOTH, expand=True)

        self._error_variable = StringVar(self._frame)

        content_frame = ttk.Frame(master=self._frame)
        content_frame.place(relx=0.5, rely=0.5,
                            anchor="center")  # Center the frame

        self._error_label = ttk.Label(
            master=content_frame,
            textvariable=self._error_variable,
            foreground="red"
        )
        self._error_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        username_label = ttk.Label(master=content_frame, text="Username")
        self._username_entry = ttk.Entry(master=content_frame, width=30)
        username_label.grid(
            row=1, column=0, sticky=constants.W, padx=5, pady=5)
        self._username_entry.grid(row=1, column=1, padx=5, pady=5)

        password_label = ttk.Label(master=content_frame, text="Password")
        self._password_entry = ttk.Entry(
            master=content_frame, width=30, show="*")
        password_label.grid(
            row=2, column=0, sticky=constants.W, padx=5, pady=5)
        self._password_entry.grid(row=2, column=1, padx=5, pady=5)

        login_button = ttk.Button(
            master=content_frame,
            text="Login",
            command=self._login_handler
        )
        create_user_button = ttk.Button(
            master=content_frame,
            text="Create user",
            command=self._handle_show_create_user_view
        )
        exit_button = ttk.Button(
            master=content_frame,
            text="Exit",
            command=self._root.quit
        )

        login_button.grid(row=3, column=0, columnspan=2,
                          padx=5, pady=5, sticky=constants.EW)
        create_user_button.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky=constants.EW)
        exit_button.grid(row=5, column=0, columnspan=2, padx=5,
                         pady=(5, 0), sticky=constants.EW)

        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)

        self._hide_error()
