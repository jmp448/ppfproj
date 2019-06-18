ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'


class BasicCourseReq:

    def __init__(self, req_name, options, position=None, course=None, satisfied=False):
        self.req_name = req_name
        self.options = options
        self.position = position
        self.course = course
        self.satisfied = satisfied

    def check_fillby(self, course):
        if self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf=None):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.course = course
        self.satisfied = True
        if ppf is not None:
            ppf[ppf_creds_col + str(self.position)] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.position)] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.position)] = course.num  # write course to ppf


class MultiCourseReq:

    def __init__(self, req_name, options, creds_needed, creds_taken=0, positions=[], courses=[], satisfied=False):
        self.req_name = req_name
        self.options = options
        self.positions = positions
        self.courses = courses
        self.creds_needed = creds_needed
        self.creds_taken = creds_taken
        self.next = 0  # used for indexing & count of completed courses
        self.satisfied = satisfied

    def check_fillby(self, course):
        for c in self.courses:
            if c.num == course.num:
                return False
        if self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf=None):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.courses.append(course)
        self.creds_taken += course.creds
        if ppf is not None:
            ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf
        if self.creds_taken >= self.creds_needed:
            self.satisfied = True
        else:
            self.next += 1
