import database

class User:
    def __init__(self, userID = None):
        if not userID:
            result = database.check_privacy(userID)
            self.userID = result[0]