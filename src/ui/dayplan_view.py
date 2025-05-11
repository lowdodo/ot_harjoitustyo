from tkinter import ttk, constants, messagebox, simpledialog


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
        self._frame = ttk.Frame(master=self._root)
        self._frame.pack(fill=constants.BOTH, expand=True)

        content_frame = ttk.Frame(master=self._frame, padding=20)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ttk.Label(
            master=content_frame, text="Day-plan", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)

        user_info_label = ttk.Label(
            master=content_frame,
            text=f"Logged in as: {self._logged_in_user.username}",
            font=("Arial", 14))
        user_info_label.pack(pady=5)

        self._task_tree = ttk.Treeview(
            content_frame,
            columns=("Name", "Type", "Start", "Duration"),
            show="headings",
            height=10
        )
        for col in ["Name", "Type", "Start", "Duration"]:
            self._task_tree.heading(col, text=col)
            self._task_tree.column(col, width=120)
        self._task_tree.pack(pady=10)

        self._task_tree.bind("<Double-1>", self._edit_selected_task)

        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Add Plans", command=self._show_add_plans_view).grid(
            row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="View Timeline",
                   command=self._show_timeline_view).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete All Tasks",
                   command=self._delete_all_tasks).grid(row=0, column=2, padx=5)

        style = ttk.Style()
        style.configure("Exit.TButton", foreground="white",
                        background="#d9534f")
        style.map("Exit.TButton",
                  background=[('active', '#c9302c'), ('!active', '#d9534f')])

        exit_button = ttk.Button(
            content_frame, text="Exit", command=self._root.quit, style="Exit.TButton")
        exit_button.pack(pady=(10, 0), fill=constants.X)

    def _load_tasks(self):
        for item in self._task_tree.get_children():
            self._task_tree.delete(item)

        self._tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)

        for task in self._tasks:
            self._task_tree.insert("", "end", iid=task.task_id, values=(
                task.name,
                task.type,
                task.start_time if task.start_time else "-",
                task.duration_minutes
            ))

    def _delete_all_tasks(self):
        confirm = messagebox.askyesno("Confirm", "Delete all tasks?")
        if confirm:
            self._dayplan_service.delete_all_tasks_for_user(
                self._logged_in_user.user_id)
            self._load_tasks()

    def _edit_selected_task(self, event):
        selected = self._task_tree.focus()
        if not selected:
            return

        task_id = selected
        task = next((t for t in self._tasks if str(
            t.task_id) == task_id), None)
        if not task:
            return

        new_name = simpledialog.askstring(
            "Edit Task", "Task name:", initialvalue=task.name)
        if not new_name:
            return

        new_duration = simpledialog.askinteger(
            "Edit Duration", "Duration (minutes):", initialvalue=task.duration_minutes)
        if new_duration is None:
            return

        new_start = simpledialog.askstring(
            "Edit Start Time", "Start time (HH:MM or empty):", initialvalue=task.start_time or "")
        if new_start == "":
            new_start = None

        task.name = new_name
        task.duration_minutes = new_duration
        task.start_time = new_start

        self._dayplan_service.update_task(task)
        self._load_tasks()
