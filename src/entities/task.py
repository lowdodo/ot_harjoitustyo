class Task:
    """Class for tasks of the day

    Attributes:
        task_id: id of the created task
        user_id: id of the user that the task is connected to
        name: name of the task
        type: what kind of task it is
        start_time: optional start time for the task
        duration_minutes: how long the task takes, in minutes

    """

    def __init__(self, task_id=None,
                 user_id=None,
                 name="",
                 type="open_time",
                 start_time=None,
                 duration_minutes=0):
        """Constructor for the class

        Args:
            task_id:
                is generated automaticly
            user_id:
                comes from the user than creates the task
            name:
                given by the user
            type:
                either set, open or passive,
                represents if something has to be done then,
                whenever or at the same time than something else
            start_time:
                optional, unles set time, when the tasks starts
            duration:
                how long the task takes to complete


        """
        self.task_id = task_id
        self.user_id = user_id
        self.name = name
        self.type = type  # settime, opentime, passive
        self.start_time = start_time
        self.duration_minutes = duration_minutes
