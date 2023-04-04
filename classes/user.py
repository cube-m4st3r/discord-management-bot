import database
class User:
    def __init__(self, userID = None):
        if userID:
            self.gradeList = database.get_grade_list_from_userID(userID)

    def get_gradeList(self):
        return self.gradeList
