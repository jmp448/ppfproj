import numpy as np

class CourseReq(object):
	def __init__(self,req_name=None,taken=False,class_name=None,grade=None,creds=None):
		self.req_name = req_name
		self.taken = taken
		self.class_name = class_name
		self.grade = grade
		self.creds = creds

	def fillby(self,course=None):
		self.taken = True
		self.class_name = course.course_num
		self.grade = course.grade
		self.creds = course.creds
