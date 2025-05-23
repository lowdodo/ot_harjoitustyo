from tkinter import ttk, constants, StringVar, IntVar, messagebox
from datetime import datetime
from entities.task import Task


class AddPlansView:
    def __init__(self, root, logged_in_user, dayplan_service, show_timeline_view, show_dayplan_view):
        self._root = root
        self._frame = None
        self._logged_in_user = logged_in_user
        self._dayplan_service = dayplan_service
        self._show_timeline_view = show_timeline_view
        self._show_dayplan_view = show_dayplan_view

        self._tasks = []
        self._total_duration = 0

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._frame.pack(fill=constants.BOTH, expand=True)

        content_frame = ttk.Frame(master=self._frame, padding=20)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(content_frame, text="Add Day Plan", font=(
            "Arial", 18, "bold")).grid(columnspan=2, pady=10)

        self.name_var = StringVar()
        self.type_var = StringVar(value="set_time")
        self.time_var = StringVar()
        self.duration_var = IntVar()

        ttk.Label(content_frame, text="Task Name:").grid(
            row=1, column=0, sticky=constants.W, padx=5, pady=2)
        ttk.Entry(content_frame, textvariable=self.name_var).grid(
            row=1, column=1, padx=5, pady=2)

        ttk.Label(content_frame, text="Task Type:").grid(
            row=2, column=0, sticky=constants.W, padx=5, pady=2)
        ttk.Combobox(content_frame, values=["set_time", "open_time", "passive"],
                     textvariable=self.type_var, state="readonly").grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(content_frame, text="Start Time (HH:MM):").grid(
            row=3, column=0, sticky=constants.W, padx=5, pady=2)
        ttk.Entry(content_frame, textvariable=self.time_var).grid(
            row=3, column=1, padx=5, pady=2)

        ttk.Label(content_frame, text="Duration (min):").grid(
            row=4, column=0, sticky=constants.W, padx=5, pady=2)
        ttk.Entry(content_frame, textvariable=self.duration_var).grid(
            row=4, column=1, padx=5, pady=2)

        ttk.Button(content_frame, text="Add Task", command=self._add_task).grid(
            row=5, columnspan=2, pady=10)

        self.task_listbox = ttk.Treeview(content_frame, columns=(
            "Name", "Type", "Start", "Duration"), show="headings", height=6)
        for col in ["Name", "Type", "Start", "Duration"]:
            self.task_listbox.heading(col, text=col)
        self.task_listbox.grid(row=6, columnspan=2,
                               pady=10, sticky=constants.EW)

        ttk.Button(content_frame, text="Save All Tasks",
                   command=self._save_tasks).grid(row=7, columnspan=2, pady=5)
        ttk.Button(content_frame, text="Back to Day Plan",
                   command=self._go_back_to_dayplan).grid(row=8, columnspan=2, pady=5)

        style = ttk.Style()
        style.configure("Exit.TButton", foreground="white",
                        background="#d9534f")
        style.map("Exit.TButton",
                  background=[('active', '#c9302c'), ('!active', '#d9534f')])

        ttk.Button(content_frame, text="Exit", command=self._root.quit, style="Exit.TButton").grid(
            row=9, columnspan=2, pady=(10, 0), sticky=constants.EW)

    def _add_task(self):
        name = self.name_var.get()
        task_type = self.type_var.get()
        start_time = self.time_var.get()
        duration = self.duration_var.get()

        if not name or not task_type or not duration:
            messagebox.showerror(
                "Error", "Please fill in all required fields.")
            return

        if task_type == "set_time":
            try:
                start_time is not None
            except ValueError:
                messagebox.showerror(
                    "Error", "set time must contain a starting time. Add the time or change task type"
                )

        if start_time:
            try:
                datetime.strptime(start_time, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Error", "Start time must be in HH:MM format.")
                return

        if self._total_duration + int(duration) > 720:
            messagebox.showerror(
                "No more time in the day")
            return

        self._tasks.append({
            "name": name,
            "type": task_type,
            "start_time": start_time,
            "duration": int(duration)
        })

        self._total_duration += int(duration)

        self.task_listbox.insert("", "end", values=(
            name, task_type, start_time or "-", duration))

        self.name_var.set("")
        self.time_var.set("")
        self.duration_var.set("")

    def _save_tasks(self):
        if not self._tasks:
            messagebox.showinfo("No Tasks", "No tasks to save.")
            return

        for task in self._tasks:
            task_obj = Task(
                user_id=self._logged_in_user.user_id,
                name=task["name"],
                type=task["type"],
                start_time=task["start_time"],
                duration_minutes=task["duration"]
            )

            self._dayplan_service.create_task(task_obj)

        messagebox.showinfo("Success", "Tasks successfully saved!")
        self._tasks.clear()
        self.task_listbox.delete(*self.task_listbox.get_children())
        self._total_duration = 0

        self.destroy()
        self._show_dayplan_view(self._logged_in_user)

    def _go_back_to_dayplan(self):
        """Navigate back to the Day Plan view without saving tasks."""
        self.destroy()
        self._show_dayplan_view(self._logged_in_user)
