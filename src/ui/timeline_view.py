from tkinter import ttk, constants, Canvas, Frame, Label
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

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)
        self._load_tasks()

    def destroy(self):
        self._frame.destroy()

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
                             height=600, scrollregion=(0, 0, 800, 960))
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        ttk.Button(content_frame, text="Suggest Timetable",
                   command=self._suggest_timetable).pack(pady=5)
        ttk.Button(content_frame, text="Back",
                   command=self._go_back_to_dayplan).pack(pady=5)
        ttk.Button(content_frame, text="Exit",
                   command=self._root.quit).pack(pady=5)

    def _go_back_to_dayplan(self):
        """Navigate back to the Day Plan view, hide current view."""
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

        for task in self._tasks:
            if task.start_time:
                start = datetime.strptime(task.start_time, "%H:%M")
                start_y = start.hour * 40 + (start.minute / 60) * 40
            else:
                start_y = 0

            height = max((task.duration_minutes / 60) * 40, 30)

            rect = self.canvas.create_rectangle(
                60, start_y, 300, start_y + height, fill="#cce5ff", tags="draggable")
            text = self.canvas.create_text(
                65, start_y + 5, text=task.name, anchor="nw", font=("Arial", 10, "bold"))

            self._task_rects[rect] = {
                "task": task,
                "text": text,
                "height": height
            }

    def _on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self._task_rects:
            self._drag_data["item"] = item
            coords = self.canvas.coords(item)
            self._drag_data["y_offset"] = event.y - coords[1]

    def _on_drag(self, event):
        item = self._drag_data["item"]
        if item:
            height = self._task_rects[item]["height"]
            new_y = event.y - self._drag_data["y_offset"]
            new_y = max(0, min(new_y, 500 - height))

            self.canvas.coords(item, 60, new_y, 300, new_y + height)
            self.canvas.coords(self._task_rects[item]["text"], 65, new_y + 5)

    def _on_release(self, event):
        item = self._drag_data["item"]
        if item:
            task = self._task_rects[item]["task"]

            if task.type == "set_time":
                print(
                    f"Task '{task.name}' is of type 'set_time', time cannot be changed.")
                self._drag_data = {"item": None, "y_offset": 0}
                return

            new_y = self.canvas.coords(item)[1]
            new_minutes = (new_y / 40) * 60  # Convert to minutes
            new_time = (datetime(2000, 1, 1) +
                        timedelta(minutes=new_minutes)).strftime("%H:%M")

            task.start_time = new_time
            self._dayplan_service.update_task_start_time(
                task.task_id, new_time)

            self._recheck_collisions_and_update_positions()

        self._drag_data = {"item": None, "y_offset": 0}

    def _recheck_collisions_and_update_positions(self):
        self.canvas.delete("all")
        self._task_rects.clear()

        for hour in range(24):
            y = hour * 40
            self.canvas.create_line(50, y, 800, y, fill="#ddd")
            self.canvas.create_text(30, y, text=f"{hour:02d}:00", anchor="e")

        occupied = [False] * (24 * 60)

        for task in self._tasks:
            start_dt = datetime.strptime(task.start_time, "%H:%M")
            start_min = start_dt.hour * 60 + start_dt.minute
            dur_min = task.duration_minutes

            start_y = (start_min / 60) * 40
            height = max((dur_min / 60) * 40, 30)

            overlapping_count = 0
            for rect_info in self._task_rects.values():
                existing_task = rect_info["task"]
                existing_y1 = self.canvas.coords(rect_info["text"])[1] - 5
                existing_y2 = existing_y1 + rect_info["height"]

                if not (start_y + height <= existing_y1 or start_y >= existing_y2):
                    overlapping_count += 1

            max_columns = 3
            slot_width = (300 - 60 - (10 * (max_columns - 1))) / max_columns
            x1 = 60 + overlapping_count * (slot_width + 10)
            x2 = x1 + slot_width

            rect = self.canvas.create_rectangle(
                x1, start_y, x2, start_y + height,
                fill="#ccffcc" if task.type == "passive" else "#cce5ff",
                tags="draggable"
            )
            text = self.canvas.create_text(
                x1 + 5, start_y + 5, text=task.name, anchor="nw", font=("Arial", 10, "bold")
            )

            self._task_rects[rect] = {
                "task": task,
                "text": text,
                "height": height
            }

        for rect_info in self._task_rects.values():
            task = rect_info["task"]
            start_dt = datetime.strptime(task.start_time, "%H:%M")
            start_min = start_dt.hour * 60 + start_dt.minute
            occupied[start_min:start_min +
                     task.duration_minutes] = [True] * task.duration_minutes

    def _suggest_timetable(self):
        self._tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)
        self.canvas.delete("all")
        self._task_rects.clear()

        for hour in range(24):
            y = hour * 40
            self.canvas.create_line(50, y, 800, y, fill="#ddd")
            self.canvas.create_text(30, y, text=f"{hour:02d}:00", anchor="e")

        type_mapping = {
            "set_time": "fixed",
            "open_time": "open",
            "passive": "passive"
        }

        fixed_tasks, open_tasks, passive_tasks = [], [], []

        for task in self._tasks:
            mapped_type = type_mapping.get(task.type)
            if mapped_type == "fixed":
                fixed_tasks.append(task)
            elif mapped_type == "open":
                open_tasks.append(task)
            elif mapped_type == "passive":
                passive_tasks.append(task)

        occupied = [False] * (24 * 60)

        for task in fixed_tasks:
            # If the task type is "set_time", start time cannot be modified
            if task.type == "set_time":
                start_dt = datetime.strptime(task.start_time, "%H:%M")
                start_min = start_dt.hour * 60 + start_dt.minute
                dur_min = task.duration_minutes

                for i in range(start_min, start_min + dur_min):
                    if 0 <= i < len(occupied):
                        occupied[i] = True

                start_y = (start_min / 60) * 40
                height = max((dur_min / 60) * 40, 30)
                self._draw_task(task, start_y, height)
                continue

            dur_min = task.duration_minutes
            found = False
            for start_min in range(9 * 60, 20 * 60 - dur_min):
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
                print(f"No room for task: {task.name}")

        passive_y = 0
        for task in passive_tasks:
            dur = task.duration_minutes
            height = max((dur / 60) * 40, 30)
            task.start_time = (datetime(2000, 1, 1) +
                               timedelta(minutes=passive_y)).strftime("%H:%M")
            self._dayplan_service.update_task_start_time(
                task.task_id, task.start_time)
            self._draw_task(task, passive_y, height)
            passive_y += 20

        print(passive_tasks, fixed_tasks, open_tasks)

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
