class User:
    """Class for user

    Attributes:
        user_id: id of the user to connect to tasks
        nusername: name for user
        password: password to protect the userinfo

    """

    def __init__(self, user_id=None, username="", password=""):
        """Constructor for the class

        Args:
            user_id:
                is created when a user is created
            username:
                given by the user
            password:
                given by the user

        """
        self.user_id = user_id
        self.username = username
        self.password = password
