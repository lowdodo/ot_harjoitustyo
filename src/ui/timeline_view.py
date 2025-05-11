from tkinter import ttk, constants, Canvas, Frame, Label, IntVar
from datetime import datetime, timedelta

# source https://www.plus2net.com/python/tkinter-drag-and-drop.php


class TaskTimelineView:
    def __init__(self, root, logged_in_user, dayplan_service, show_dayplan_view):
        self._root = root
        self._frame = None
        self._logged_in_user = logged_in_user
        self._dayplan_service = dayplan_service
        self._show_dayplan_view = show_dayplan_view

        self._tasks = []
        self._task_rects = {}
        self._drag_data = {"item": None, "y_offset": 0}

        self.start_hour_var = IntVar(value=8)
        self.end_hour_var = IntVar(value=21)

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)
        self._load_tasks()

    def destroy(self):
        self._frame.destroy()

#timelinen tyylittelyyn ja scrollattavuuteen käytetty apuna chatgpt:tä
    def _initialize(self):
        self._frame = Frame(master=self._root)
        self._frame.pack(fill=constants.BOTH, expand=True)

        content_frame = Frame(self._frame, padx=20, pady=20)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(content_frame, text="Task Timeline (Today)",
              font=("Arial", 20, "bold")).pack(pady=10)

        canvas_frame = Frame(content_frame)
        canvas_frame.pack(fill=constants.BOTH, expand=True)

        self.canvas = Canvas(canvas_frame, bg="white", width=800,
                             height=600, scrollregion=(0, 0, 700, 960))
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self.suggest_button = ttk.Button(content_frame, text="Suggest Timetable", command=self._suggest_timetable)
        self.suggest_button.pack(pady=5)

        self.save_button = ttk.Button(content_frame, text="Save Suggestion", command=self._save_suggestion)

        ttk.Label(content_frame, text="Suggestion start hour:").pack()
        ttk.Spinbox(content_frame, from_=0, to=23, textvariable=self.start_hour_var, width=5).pack()

        ttk.Label(content_frame, text="Suggestion end hour:").pack()
        ttk.Spinbox(content_frame, from_=1, to=24, textvariable=self.end_hour_var, width=5).pack()

        ttk.Button(content_frame, text="Back",
                   command=self._go_back_to_dayplan).pack(pady=5)
        
        style = ttk.Style()
        style.configure("Exit.TButton", foreground="white", background="#d9534f")
        style.map("Exit.TButton",
                  background=[('active', '#c9302c'), ('!active', '#d9534f')])

        ttk.Button(content_frame, text="Exit",
                   command=self._root.quit, style="Exit.TButton").pack(pady=5)

        self.status_label = Label(content_frame, text="", fg="red", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def _go_back_to_dayplan(self):
        self.destroy()
        self._show_dayplan_view(self._logged_in_user)

    def _load_tasks(self):
        self.canvas.delete("all")
        self._tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)
        self._task_rects.clear()

        for hour in range(24):
            y = hour * 40
            self.canvas.create_line(50, y, 800, y, fill="#ddd")
            self.canvas.create_text(30, y, text=f"{hour:02d}:00", anchor="e")

        for idx, task in enumerate(self._tasks):
            if task.start_time:
                start = datetime.strptime(task.start_time, "%H:%M")
                start_y = start.hour * 40 + (start.minute / 60) * 40
            else:
                start_y = idx * 35

            height = max((task.duration_minutes / 60) * 40, 30)

            self._draw_task(task, start_y, height)

    def _on_click(self, event):
        canvas_y = self.canvas.canvasy(event.y)
        item = self.canvas.find_closest(event.x, canvas_y)[0]
        if item in self._task_rects:
            self._drag_data["item"] = item
            coords = self.canvas.coords(item)
            self._drag_data["y_offset"] = canvas_y - coords[1]

    def _on_drag(self, event):
        item = self._drag_data["item"]
        if item:
            height = self._task_rects[item]["height"]
            canvas_y = self.canvas.canvasy(event.y)
            new_y = canvas_y - self._drag_data["y_offset"]
            new_y = max(0, min(new_y, 960 - height))
            self.canvas.coords(item, 60, new_y, 300, new_y + height)
            self.canvas.coords(self._task_rects[item]["text"], 65, new_y + 5)

    def _on_release(self, event):
        item = self._drag_data["item"]
        if item:
            task = self._task_rects[item]["task"]

            if task.type == "set_time":
                self.status_label.config(text=f"Task '{task.name}' is of type 'set_time', time cannot be changed.")
                self._drag_data = {"item": None, "y_offset": 0}
                self._load_tasks()
                return

            canvas_y = self.canvas.canvasy(event.y)
            new_y = self.canvas.coords(item)[1]
            new_minutes = (new_y / 40) * 60
            new_time = (datetime(2000, 1, 1) + timedelta(minutes=new_minutes)).strftime("%H:%M")

            task.start_time = new_time
            self._dayplan_service.update_task_start_time(task.task_id, new_time)

        self._drag_data = {"item": None, "y_offset": 0}
        self._load_tasks()

    def _suggest_timetable(self):
        self._tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)
        self.canvas.delete("all")
        self._task_rects.clear()

        for hour in range(24):
            y = hour * 40
            self.canvas.create_line(50, y, 800, y, fill="#ddd")
            self.canvas.create_text(30, y, text=f"{hour:02d}:00", anchor="e")

        set_time_tasks = [t for t in self._tasks if t.type == "set_time"]
        open_time_tasks = [t for t in self._tasks if t.type == "open_time"]
        passive_tasks = [t for t in self._tasks if t.type == "passive"]

        occupied = [False] * (24 * 60)

        for task in set_time_tasks:
            start_dt = datetime.strptime(task.start_time, "%H:%M")
            start_min = start_dt.hour * 60 + start_dt.minute
            dur_min = task.duration_minutes
            for i in range(start_min, start_min + dur_min):
                if 0 <= i < len(occupied):
                    occupied[i] = True
            start_y = (start_min / 60) * 40
            height = max((dur_min / 60) * 40, 30)
            self._draw_task(task, start_y, height)

        start_hour = self.start_hour_var.get()
        end_hour = self.end_hour_var.get()
        if start_hour >= end_hour:
            self.status_label.config(text="Start hour must be before end hour.")
            return

        earliest = start_hour * 60
        latest = end_hour * 60 - dur_min

        for task in open_time_tasks:
            dur_min = task.duration_minutes
            found = False
            for start_min in range(earliest, latest + 1):
                if all(not occupied[i] for i in range(start_min, start_min + dur_min)):
                    for i in range(start_min, start_min + dur_min):
                        occupied[i] = True
                    task.start_time = (datetime(2000, 1, 1) +
                                    timedelta(minutes=start_min)).strftime("%H:%M")
                    self._dayplan_service.update_task_start_time(
                        task.task_id, task.start_time)
                    start_y = (start_min / 60) * 40
                    height = max((dur_min / 60) * 40, 30)
                    self._draw_task(task, start_y, height)
                    found = True
                    break
            if not found:
                task.start_time = None
                self._dayplan_service.update_task_start_time(task.task_id, None)
                self.status_label.config(text=f"No room for task: {task.name}")
                start_y = 850 + len(self._task_rects) * 45
                height = max((task.duration_minutes / 60) * 40, 30)
                self._draw_task(task, start_y, height)

        passive_y = 20 * 60
        for task in passive_tasks:
            dur = task.duration_minutes
            height = max((dur / 60) * 40, 30)
            task.start_time = (datetime(2000, 1, 1) +
                            timedelta(minutes=passive_y)).strftime("%H:%M")
            self._dayplan_service.update_task_start_time(
                task.task_id, task.start_time)
            self._draw_task(task, (passive_y / 60) * 40, height)
            passive_y += 20

        self.suggest_button.pack_forget()
        self.save_button.pack(pady=5)

    def _save_suggestion(self):
        for task in self._tasks:
            if task.start_time:
                self._dayplan_service.update_task_start_time(task.task_id, task.start_time)

        self.status_label.config(text="Suggested timetable saved successfully.")

        self._load_tasks()

        self.save_button.pack_forget()
        self.suggest_button.pack(pady=5)

    def _draw_task(self, task, start_y, height):
        end_y = start_y + height
        x_start = 60
        x_end = 300
        width = x_end - x_start
        padding = 10

        overlapping_count = 0
        for rect_info in self._task_rects.values():
            existing_task = rect_info["task"]
            existing_y1 = self.canvas.coords(rect_info["text"])[1] - 5
            existing_y2 = existing_y1 + rect_info["height"]

            if not (end_y <= existing_y1 or start_y >= existing_y2):
                overlapping_count += 1

        max_columns = 3
        slot_width = (width - (padding * (max_columns - 1))) / max_columns
        x1 = x_start + overlapping_count * (slot_width + padding)
        x2 = x1 + slot_width

        rect = self.canvas.create_rectangle(
            x1, start_y, x2, end_y,
            fill="#ccffcc" if task.type == "passive" else "#cce5ff",
            tags="draggable"
        )
        text = self.canvas.create_text(
            x1 + 5, start_y + 5, text=task.name, anchor="nw", font=("Arial", 10, "bold"))

        self._task_rects[rect] = {
            "task": task,
            "text": text,
            "height": height
        }
