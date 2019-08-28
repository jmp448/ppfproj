from support_files.helper_tools import exceeds, categories_represented
from support_files.web_reader import get_full_libarts_dict
import re
from copy import deepcopy

ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'
ppf_categories_col = 'H'
ppf_description_col = 'B'

libart_dict = get_full_libarts_dict()


class BasicCourseReq:

    def __init__(self, req_name, options, threshold=None, position=None, course=None, satisfied=False, ap_satisfied=False):
        self.req_name = req_name
        self.options = options
        self.threshold = threshold
        self.position = position
        self.course = course
        self.satisfied = satisfied
        self.ap_satisfied = ap_satisfied

    def check_fillby(self, c):
        # Check that course hasn't been taken before
        if self.course is not None:
            if self.course.num == c.num:
                return False
            if self.course.ap and c.ap:
                # Can't replace an AP with another AP
                return False

        # Check if the course meets the requirement
        if not self.options.__contains__(c.num):
            return False

        # Upcoming semester courses will be written in
        if c.grade is None and self.options.__contains__(c.num):
            return True

        # Check if the grade meets the threshold
        no_no_list = ['S', 'U', 'SX', 'UX', 'W', 'INC', 'NGR', 'F']
        if no_no_list.__contains__(c.grade) and not c.ap:
            return False

        # Otherwise, let it fly
        return True

    def fillby(self, course, ppf):
        assert self.check_fillby(course), "%s cannot be satisfied by %s" % (self.req_name, course.num)
        self.course = course
        if course.grade is None and not course.ap:
            ppf[ppf_creds_col + str(self.position)] = course.creds  # write credits to ppf
            ppf[ppf_grade_col + str(self.position)] = course.term  # write term to ppf
            ppf[ppf_course_col + str(self.position)] = course.num  # write course to ppf
        elif course.ap:
            self.satisfied = True
            self.ap_satisfied = True
            if ppf is not None:
                ppf[ppf_creds_col + str(self.position)] = course.creds  # write credits to ppf
                ppf[ppf_grade_col + str(self.position)] = "AP"  # write grade to ppf
                ppf[ppf_course_col + str(self.position)] = course.ap_ppf_desc  # write course to ppf
                if self.req_name == "Thermodynamics":
                    ppf[ppf_course_col + str(self.position+1)] = None
        else:
            self.satisfied = True
            if ppf is not None:
                ppf[ppf_creds_col + str(self.position)] = course.creds  # write credits to ppf
                ppf[ppf_grade_col + str(self.position)] = course.grade  # write grade to ppf
                ppf[ppf_course_col + str(self.position)] = course.num  # write course to ppf
                if self.req_name == "Thermodynamics":
                    ppf[ppf_course_col + str(self.position+1)] = None


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

        # Check that course hasn't been taken before
        if self.courses is not None:
            for c in self.courses:
                if c.num == course.num:
                    return False

        # Check that there's room for the course
        if self.courses is not None:
            if len(self.positions) <= self.next:
                # Can't take more courses in a category than there are slots
                return False

        # Upcoming semester courses will be written in
        if course.grade is None and (override or self.options.__contains__(course.num)):
            return True

        # See if this course satisfies the req
        if not (override or self.options.__contains__(course.num)):
            return False

        # Check that the course meets the grade threshold
        if self.libart:
            no_no_list = ['U', 'UX', 'W', 'INC', 'NGR', 'F']
        else:
            no_no_list = ['S', 'U', 'SX', 'UX', 'W', 'INC', 'NGR', 'F']
        if course.grade in no_no_list:
            return False

        # Make sure the course is necessary
        if self.courses is not None and self.libart:  # some stricter reqs to make sure a liberal arts course is necesssary
            # Over 2000s shouldn't exceed 4
            if not course.ap:
                assert(len(re.findall(r'\d+', course.num)) == 1), "Error reading course number: %s" % course.num
                c_num = int(re.findall(r'\d+', course.num)[0])
            under2000s = 0
            for c in self.courses:
                if c.ap:
                    under2000s += 1
                else:
                    assert (len(re.findall(r'\d+', c.num)) == 1), "Error reading course number: %s" % c.num
                    if int(re.findall(r'\d+', c.num)[0]) < 2000:
                        under2000s += 1
            if under2000s >= 4 and (c.ap or c_num < 2000):
                return False

            # Eventually have to cover at least 3 categories
            curr_courses = deepcopy(self.courses)
            course.categories = libart_dict[course.num]
            curr_courses.append(course)
            if len(curr_courses) - categories_represented(curr_courses) > 3:
                return False

        # Otherwise, let it pass
        return True

    def fillby(self, course, ppf, override=False, include_desc=False):
        assert self.check_fillby(course, override), "%s cannot be satisfied by %s" % (self.req_name, course.num)

        if self.courses is None:
            self.courses = [course]
        else:
            self.courses.append(course)

        if course.grade is None and not course.ap:
            if ppf is not None:
                ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
                ppf[ppf_grade_col + str(self.positions[self.next])] = course.term  # write term to ppf
                ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf


        elif course.ap:
            self.creds_taken += course.creds
            if ppf is not None:
                ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
                ppf[ppf_grade_col + str(self.positions[self.next])] = "AP"  # write term to ppf
                ppf[ppf_course_col + str(self.positions[self.next])] = course.ap_ppf_desc  # write course to ppf

        else:
            self.creds_taken += course.creds
            if ppf is not None:
                ppf[ppf_creds_col + str(self.positions[self.next])] = course.creds  # write credits to ppf
                ppf[ppf_grade_col + str(self.positions[self.next])] = course.grade  # write grade to ppf
                ppf[ppf_course_col + str(self.positions[self.next])] = course.num  # write course to ppf

        if include_desc:
            ppf[ppf_description_col + str(self.positions[self.next])] = course.desc

        if self.creds_taken >= self.creds_needed and not self.libart:
            self.satisfied = True

        elif self.libart:
            # Fill in liberal studies courses' extra info (category and description)
            course.categories = libart_dict[course.num]
            assert len(course.categories) >= 1, "%s has been listed as a lib art course mistakenly" % course.num
            cat = ""
            for l in course.categories:
                cat += "%s, " % l
            cat = cat[:-2]  # just trimming away the last comma and space
            ppf[ppf_categories_col + str(self.positions[self.next])] = cat
            ppf[ppf_description_col + str(self.positions[self.next])] = course.desc

            # Additional criteria for satisfying liberal studies requirement
            # At least two courses at or above 2000 level
            if not course.ap:
                assert (len(re.findall(r'\d+', course.num)) == 1), "Error reading course number: %s" % course.num
                c_num = int(re.findall(r'\d+', course.num)[0])
                if c_num >= 2000:
                    self.over2000s += 1
            test1 = self.over2000s >= 2

            # Courses from at least 3 categories
            test2 = categories_represented(self.courses) >= 3

            # 18 credits
            test3 = self.creds_taken >= self.creds_needed
            if test1 and test2 and test3:
                self.satisfied = True

        if not self.satisfied:
            self.next += 1


class ApprovedElectives:
    def __init__(self):
        self.courses = None
        self.creds = 0
        self.next = 93
        self.loc = 'M95'
        self.min_creds = 6

    def check_fillby(self, course):

        failing_grades = ['U', 'UX', 'W', 'INC', 'NGR', 'F']

        # cannot use AP courses
        if course.ap:
            return False
        # dismiss failed or incompleted courses
        elif failing_grades.__contains__(course.grade):
            return False
        # cannot use 10XX courses (ie MATH1091)
        assert (len(re.findall(r'\d+', course.num)) == 1), "Error reading course number: %s" % course.num
        c_num = re.findall(r'\d+', course.num)[0][:2]
        if c_num == "10":
            return False
        # cannot use more than 6 credits or 3 courses
        elif self.creds >= 6 or self.next >= 96:
            return False
        # cannot use PE courses
        elif course.num[:2] == "PE":
            return False
        else:
            return True

    def fillby(self, course, ppf):
        assert self.check_fillby(course), "%s cannot be used as an approved elective" % course.num
        if self.courses is None:
            self.courses = [course]
        else:
            self.courses.append(course)
        ppf[ppf_description_col+str(self.next)] = course.desc
        ppf[ppf_course_col+str(self.next)] = course.num
        ppf[ppf_grade_col+str(self.next)] = course.grade
        ppf[ppf_creds_col+str(self.next)] = course.creds
        self.next += 1
