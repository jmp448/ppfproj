from helper_tools import exceeds

ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'


class BasicCourseReq:

    def __init__(self, req_name, options, threshold=None, position=None, course=None, satisfied=False):
        self.req_name = req_name
        self.options = options
        self.threshold = threshold
        self.position = position
        self.course = course
        self.satisfied = satisfied

    def check_fillby(self, course):
        if self.options.__contains__(course.num):
            if self.threshold is None:
                return True
            elif exceeds(course.grade, self.threshold):
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

    def check_fillby(self, course, override=False):
        for c in self.courses:
            if c.num == course.num:
                return False
        if override:
            return True
        elif self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf=None, override=False, extra_reqs=False):
        assert self.check_fillby(course, override), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.courses.append(course)
        self.creds_taken += course.creds
        if ppf is not None:
            ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf
        if self.creds_taken >= self.creds_needed and not extra_reqs:
            self.satisfied = True
        else:
            self.next += 1


class FillinCourseReq:
    '''
    This is used for advanced bio and focus areas, when the number of courses is simply determined by how many credits
    the student has left to finish a certain category
    '''

    def __init__(self, req_name, options, category, positions=[], courses=[], satisfied=False):
        self.req_name = req_name
        self.options = options
        self.category = category
        self.positions = positions
        self.courses = courses
        self.next = 0  # used for indexing & count of completed courses
        self.satisfied = satisfied

    def check_fillby(self, course):
        # See if the course has already been used for this requirement
        for c in self.courses:
            if c.num == course.num:
                return False
        # Check to see whether the course satisfies the requirement
        if self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf=None):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.courses.append(course)
        if ppf is not None:
            ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf
        if self.category.curr_creds >= self.category.min_creds:
            self.satisfied = True
        else:
            self.next += 1
