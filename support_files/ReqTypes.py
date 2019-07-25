from support_files.helper_tools import exceeds, categories_represented
from support_files.web_reader import get_full_libarts_dict

ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'
ppf_categories_col = 'H'
ppf_description_col = 'B'

libart_dict = get_full_libarts_dict()


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

    def fillby(self, course, ppf):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.course = course
        self.satisfied = True
        if ppf is not None:
            ppf[ppf_creds_col + str(self.position)] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.position)] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.position)] = course.num  # write course to ppf


class MultiCourseReq:

    def __init__(self, req_name, options, creds_needed, positions, creds_taken=0, courses=None, satisfied=False,
                 over2000s=0, libart=False):
        self.req_name = req_name
        self.options = options
        self.positions = positions
        self.courses = courses
        self.creds_needed = creds_needed
        self.creds_taken = creds_taken
        self.next = 0  # used for indexing & count of completed courses
        self.satisfied = satisfied
        self.over2000s = over2000s
        self.libart = libart

    def check_fillby(self, course, override=False):
        # Check that course hasn't been taken
        if self.courses is not None:
            for c in self.courses:
                if c.num == course.num:
                    return False
        # Special cases
        if override:
            return True
        # See if this course satisfies the req
        elif self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf, override=False):
        assert self.check_fillby(course, override), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        if self.courses is None:
            self.courses = [course]
        else:
            self.courses.append(course)
        self.creds_taken += course.creds
        if ppf is not None:
            ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf
        if self.creds_taken >= self.creds_needed and not self.libart:
            self.satisfied = True
        elif self.libart:
            # Fill in liberal studies courses' extra info (category and description)
            course.categories = libart_dict[course.num]
            assert len(course.categories) >= 1, "%s has been listed as a lib art course mistakenly" % course.num
            cat = ""
            for l in course.categories:
                cat += "%s, " % l
            cat = cat[:-2]
            ppf[ppf_categories_col + str(self.positions[self.next])] = cat
            ppf[ppf_description_col + str(self.positions[self.next])] = course.desc

            # Additional criteria for satisfying liberal studies requirement
            # At least two courses at or above 2000 level
            test1 = self.over2000s >= 2
            # Courses from at least 3 categories
            test2 = categories_represented(self.courses) >= 3
            # 18 credits
            test3 = self.creds_taken >= self.creds_needed
            if test1 and test2 and test3:
                self.satisfied = True
                print("Satisfied lib arts")
        if not self.satisfied:
            self.next += 1


class FillinCourseReq:
    '''
    This is used for advanced bio and focus areas, when the number of courses is simply determined by how many credits
    the student has left to finish a certain category
    '''

    def __init__(self, req_name, options, category, positions, courses=None, satisfied=False):
        self.req_name = req_name
        self.options = options
        self.category = category
        self.positions = positions
        self.courses = courses
        self.next = 0  # used for indexing & count of completed courses
        self.satisfied = satisfied

    def check_fillby(self, course):
        # See if the course has already been used for this requirement
        if self.courses is not None:
            for c in self.courses:
                if c.num == course.num:
                    return False
        # Check to see whether the course satisfies the requirement
        if self.options.__contains__(course.num):
            return True
        else:
            return False

    def fillby(self, course, ppf):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        if self.courses is None:
            self.courses = [course]
        else:
            self.courses.append(course)
        if ppf is not None:
            ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
            ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf
        if self.category.curr_creds >= self.category.min_creds:
            self.satisfied = True
        else:
            self.next += 1
