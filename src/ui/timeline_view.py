from tkinter import ttk, constants, Canvas, Frame, Label
from datetime import datetime, timedelta

# lähteet https://www.plus2net.com/python/tkinter-drag-and-drop.php


class TaskTimelineView:
    def __init__(self, root, logged_in_user, dayplan_service, go_back_callback):
        self._root = root
        self._frame = None
        self._logged_in_user = logged_in_user
        self._dayplan_service = dayplan_service
        self._go_back_callback = go_back_callback

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
        self._frame = Frame(master=self._root, width=850,
                            height=600, padx=20, pady=20)
        self._frame.pack_propagate(False)

        Label(self._frame, text="Task Timeline (Today)",
              font=("Arial", 20, "bold")).pack(pady=10)

        self.canvas = Canvas(self._frame, bg="white", height=500)
        self.canvas.pack(fill=constants.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        back_button = ttk.Button(
            self._frame, text="Back", command=self._go_back_callback)
        back_button.pack(pady=10)

    def _load_tasks(self):
        self.canvas.delete("all")
        self._tasks = self._dayplan_service.get_tasks_for_user(
            self._logged_in_user.user_id)
        self._task_rects.clear()

        for hour in range(25):
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
            new_y = self.canvas.coords(item)[1]
            new_minutes = (new_y / 40) * 60
            new_time = (datetime(2000, 1, 1) +
                        timedelta(minutes=new_minutes)).strftime("%H:%M")

            task = self._task_rects[item]["task"]
            task.start_time = new_time
            self._dayplan_service.update_task_start_time(
                task.task_id, new_time)

        self._drag_data = {"item": None, "y_offset": 0}
