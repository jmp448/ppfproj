# Define the Course object

class Course:

    def __init__(self, num, grade, creds, term=None, desc=None, categories=None):
        self.num = num
        self.grade = grade
        self.creds = creds
        self.term = term
        self.desc = desc
        self.categories = categories
