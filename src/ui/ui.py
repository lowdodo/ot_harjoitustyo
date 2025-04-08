from ui.login_view import LoginView
from ui.create_user_view import CreateUserView
from ui.dayplan_view import DayPlanView
from ui.add_plans_view import AddPlansView
from services.dayplan_service import DayplanService


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None
        self._logged_in_user = None
        self._dayplan_service = DayplanService()

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _handle_login(self, user):
        print(f"Login successful! Logged in as: {user.username}")
        self._show_day_plan_view(user)

    def _handle_show_create_user_view(self):
        print("Navigating to the create user view.")
        self._show_create_user_view()

    def _handle_create_user(self):
        print("User created successfully!")
        self._show_login_view()

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._handle_login,
            self._handle_show_create_user_view
        )

        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(
            self._root,
            self._handle_create_user,
            self._show_login_view
        )

        self._current_view.pack()

    def _show_day_plan_view(self, user):
        self._logged_in_user = user
        self._hide_current_view()

        self._current_view = DayPlanView(
            self._root,
            user,
            self._show_add_plans_view,
            self._dayplan_service
        )
        self._current_view.pack()

    def _show_add_plans_view(self):
        self._hide_current_view()

        self._add_plans_view = AddPlansView(
            self._root, self._logged_in_user, self._dayplan_service)
        self._add_plans_view.pack()
