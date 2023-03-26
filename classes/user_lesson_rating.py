from user import User
class User_lesson_grade:
    def __init__(self, userID):
        self.user = User(userID)
        self.lesson_grade = self.user.get_gradeList()
