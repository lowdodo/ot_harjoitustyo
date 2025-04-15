from tkinter import ttk, constants


class DayPlanView:
    def __init__(self, root, logged_in_user, show_add_plans_view, dayplan_service, show_timeline_view):
        self._root = root
        self._frame = None
        self._logged_in_user = logged_in_user
        self._show_add_plans_view = show_add_plans_view
        self._dayplan_service = dayplan_service
        self._show_timeline_view = show_timeline_view
        self._task_tree = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)
        self._load_tasks()

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(
            master=self._root, width=800, height=600, padding=20)
        self._frame.pack_propagate(False)

        title_label = ttk.Label(
            master=self._frame, text="Day-plan", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        user_info_label = ttk.Label(
            master=self._frame,
            text=f"Logged in as: {self._logged_in_user.username}",
            font=("Arial", 14))
        user_info_label.pack(pady=5)

        self._task_tree = ttk.Treeview(
            self._frame,
            columns=("Name", "Type", "Start", "Duration"),
            show="headings",
            height=10
        )
        for col in ["Name", "Type", "Start", "Duration"]:
            self._task_tree.heading(col, text=col)
            self._task_tree.column(col, width=120)
        self._task_tree.pack(pady=10)

        add_plans_button = ttk.Button(
            master=self._frame,
            text="Add Plans",
            command=self._show_add_plans_view
        )
        add_plans_button.pack(pady=10)

        timeline_button = ttk.Button(
            master=self._frame,
            text="View Timeline",
            command=self._show_timeline_view
        )
        timeline_button.pack(pady=5)

    def _load_tasks(self):
        for item in self._task_tree.get_children():
            self._task_tree.delete(item)

        tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)

        for task in tasks:
            self._task_tree.insert("", "end", values=(
                task.name,
                task.type,
                task.start_time if task.start_time else "-",
                task.duration_minutes
            ))
