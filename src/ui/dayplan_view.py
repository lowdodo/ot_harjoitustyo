from tkinter import ttk, constants


class DayPlanView:
    def __init__(self, root, logged_in_user):
        self._root = root
        self._frame = None
        self._logged_in_user = logged_in_user
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root, width=600, height=400)
        self._frame.pack_propagate(False)

        title_label = ttk.Label(
            master=self._frame, text="Day-plan", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)

        user_info_label = ttk.Label(
            master=self._frame,
            text=f"Logged in as: {self._logged_in_user.username}",
            font=("Arial", 14))

        user_info_label.pack(pady=10)

        self._frame.pack(fill=constants.BOTH, expand=True)
