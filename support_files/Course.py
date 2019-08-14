"""
The course object is used to store a course that has been taken by the student
Courses will be created when they are read off of an existing PPF, an unofficial transcript, or a semester report

Course attributes include

num: the course number, including the department (ie SPAN1000)
grade: the grade received on the course (ie A-, INC)
creds: the number of credits received for the course
term: the term in which the course was taken (not defined for courses read off of a PPF)
desc: the course description (ie Introduction to Spanish Language)
categories: for liberal arts courses, a list of the categories which this course can satisfy (ie FL, LA)
ap: a boolean value for whether the course is an AP course (necessary as these are recorded differently on a ppf)
ap_name: the description of the AP that will be given in the transcript (ie "Mathematics: Calculus AB")
ap_ppf_desc: the description of the AP course that will be written on the PPF (ie "MATH AP")
"""


class Course:

    def __init__(self, num, grade, creds, term=None, desc=None, categories=None, ap=False, ap_ppf_desc=None,
                 transfer=False):
        self.num = num
        self.grade = grade
        self.creds = creds
        self.term = term
        self.desc = desc
        self.categories = categories
        self.ap = ap
        self.ap_ppf_desc = ap_ppf_desc
        self.transfer = transfer


