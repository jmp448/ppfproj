from support_files.define_reqs import create_category_list
from support_files.helper_tools import *
from shutil import copy
from support_files.ReqTypes import *
import os, re

ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'
ppf_categories_col = 'H'
ppf_description_col = 'B'
ppf_courses_unneeded_col = 'C'
ppf_grand_total = 'M98'


class Student:
    def __init__(self, transcript, row, cols, test=False, course_list=None):
        name_loc = cols['student name'] + row
        self.name = transcript[name_loc].value

        netid_loc = cols['netid'] + row
        self.netid = transcript[netid_loc].value

        studid_loc = cols['student id'] + row
        self.student_id = transcript[studid_loc].value

        self.test = test

        grad_loc = cols['grad'] + row
        self.grad = transcript[grad_loc].value
        if self.grad == "N/A":
            self.grad = "NONE"
        if " " in self.grad:
            if self.test:
                self.folder = "/Students_test/%s" % ldescr2sdescr(self.grad)
            else:
                self.folder = "/Students/%s" % ldescr2sdescr(self.grad)
        else:
            if self.test:
                self.folder = "/Students_test/%s" % self.grad
            else:
                self.folder = "/Students/%s" % self.grad

        # If the necessary folder doesn't exist yet, create it
        parent = os.getcwd()
        if not os.path.exists(parent + self.folder):
            os.mkdir(parent+self.folder)

        self.requirements = create_category_list()

        self.total_creds = 0

        self.notneeded_next = 111

        if course_list is None:
            self.course_list = []
        else:
            self.course_list = course_list

        # Check to see if student has a ppf
        parent = os.getcwd()
        has_ppf, filename = self.has_ppf()
        if has_ppf:  # if they do have a PPF, read it
            os.chdir(parent + self.folder)
            self.filename, self.wb, self.ppf = open_excel_file(filename)
            os.chdir(parent)
            self.read_ppf()
        else:  # if they don't, create a new one
            self.create_ppf()

    def has_ppf(self):
        parent = os.getcwd()
        os.chdir(parent+self.folder)

        [lname, fname] = self.name.split(',')
        filename = lname.lower() + fname[0].lower() +\
                   '-' + self.netid + '.xlsx'

        if os.path.isfile(filename):
            os.chdir(parent)
            return True, filename
        else:
            os.chdir(parent)
            return False, filename

    def create_ppf(self):
        """
        Create a new PPF for any student that does not yet have one

        Fills in name, netID, student ID, and expected graduation date
        """
        folder = os.getcwd()
        template = folder + '/blankPPF.xlsx'

        [lname, fname] = self.name.split(',')
        file = self.folder + "/" + lname.lower() + fname[0].lower() + '-' + self.netid + '.xlsx'

        file = folder + file

        copy(template, file)

        self.filename, self.wb, self.ppf = open_excel_file(file)

        # Fill student info
        self.ppf['B5'] = self.name
        self.ppf['B6'] = self.netid
        self.ppf['G6'] = self.student_id
        # ppf['L6'] = student.advisor
        self.ppf['M7'] = self.grad

        self.wb.save(filename=self.filename)

    def read_ppf(self):
        """
        Read the information contained in a student's existing PPF, and update the student's information

        Broken up by category so if only one category is misread that can be individually debugged
        """
        assert self.has_ppf(), "%s does not have a PPF yet" % self.name

        self.read_math()
        self.read_phys()
        self.read_chem()
        self.read_bio()
        self.read_fws()
        self.read_lib()
        self.read_cs()
        self.read_eng()
        self.read_approved()
        self.read_others()

    def read_math(self):
        for cat in self.requirements:
            if cat.cat_name == "Math":
                math = cat
                break
        for req in math.reqs:
            if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                self.ppf[ppf_creds_col + str(req.position)] = None
                self.ppf[ppf_grade_col + str(req.position)] = None
            elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                c = read_class_from_ppf(self.ppf, req.position)
                req.course = c
                req.satisfied = True
                math.curr_creds += int(c.creds)
                self.total_creds += int(c.creds)

    def read_phys(self):
        for cat in self.requirements:
            if cat.cat_name == "Physics":
                phys = cat
                break
        for req in phys.reqs:
            if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                self.ppf[ppf_creds_col + str(req.position)] = None
                self.ppf[ppf_grade_col + str(req.position)] = None
            elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                c = read_class_from_ppf(self.ppf, req.position)
                req.course = c
                req.satisfied = True
                phys.curr_creds += int(c.creds)
                self.total_creds += int(c.creds)

    def read_chem(self):
        for cat in self.requirements:
            if cat.cat_name == "Chemistry":
                chem = cat
                break
        for req in chem.reqs:
            if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                self.ppf[ppf_creds_col + str(req.position)] = None
                self.ppf[ppf_grade_col + str(req.position)] = None
            elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                c = read_class_from_ppf(self.ppf, req.position)
                req.course = c
                req.satisfied = True
                chem.curr_creds += int(c.creds)
                self.total_creds += int(c.creds)

    def read_bio(self):
        for cat in self.requirements:
            if cat.cat_name == "Biological Sciences":
                bio = cat
                break
        for req in bio.reqs:
            if isinstance(req, BasicCourseReq):
                if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                    self.ppf[ppf_creds_col + str(req.position)] = None
                    self.ppf[ppf_grade_col + str(req.position)] = None
                elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                    c = read_class_from_ppf(self.ppf, req.position)
                    req.course = c
                    req.satisfied = True
                    bio.curr_creds += int(c.creds)
                    self.total_creds += int(c.creds)
            elif isinstance(req, MultiCourseReq):
                for p in req.positions:
                    if is_semester(self.ppf[ppf_grade_col + str(p)].value):
                        self.ppf[ppf_creds_col + str(p)] = None
                        self.ppf[ppf_grade_col + str(p)] = None
                    elif self.ppf[ppf_creds_col + str(p)].value is not None:
                        c = read_class_from_ppf(self.ppf, p)
                        if req.courses is None:
                            req.courses = [c]
                        else:
                            req.courses.append(c)
                        req.creds_taken += int(c.creds)
                        if req.creds_taken >= req.creds_needed:
                            req.satisfied = True
                        else:
                            req.next += 1
                        bio.curr_creds += int(c.creds)
                        self.total_creds += int(c.creds)

    def read_fws(self):
        for cat in self.requirements:
            if cat.cat_name == "First-Year Writing Seminar":
                fws = cat
                break
        for req in fws.reqs:  # Only the one multi-course req
            for p in req.positions:
                if is_semester(self.ppf[ppf_grade_col + str(p)].value):
                    self.ppf[ppf_creds_col + str(p)] = None
                    self.ppf[ppf_grade_col + str(p)] = None
                elif self.ppf[ppf_creds_col + str(p)].value is not None:
                    c = read_class_from_ppf(self.ppf, p)
                    if req.courses is None:
                        req.courses = [c]
                    else:
                        req.courses.append(c)
                    req.creds_taken += int(c.creds)
                    if req.creds_taken >= req.creds_needed:
                        req.satisfied = True
                    else:
                        req.next += 1
                    fws.curr_creds += int(c.creds)
                    self.total_creds += int(c.creds)

    def read_lib(self):
        for cat in self.requirements:
            if cat.cat_name == "Liberal Studies":
                lib = cat
                break
        for req in lib.reqs:  # Only the one multi-course req
            for p in req.positions:
                if is_semester(self.ppf[ppf_grade_col + str(p)].value):
                    self.ppf[ppf_creds_col + str(p)] = None
                    self.ppf[ppf_grade_col + str(p)] = None
                elif self.ppf[ppf_creds_col + str(p)].value is not None:
                    c = read_class_from_ppf(self.ppf, p)
                    s = self.ppf['H'+str(p)].value
                    s = s.replace(" ", "")
                    s = s.split(",")
                    c.categories = s
                    if req.courses is None:
                        req.courses = [c]
                    else:
                        req.courses.append(c)
                    req.creds_taken += int(c.creds)
                    assert (len(re.findall(r'\d+', c.num)) == 1), "Error reading course number: %s" % course.num
                    c_num = int(re.findall(r'\d+', c.num)[0])
                    if c_num >= 2000:
                        req.over2000s += 1
                    test1 = req.creds_taken >= req.creds_needed
                    test2 = req.over2000s >= 1
                    test3 = categories_represented(req.courses) >= 3
                    if test1 and test2 and test3:
                        req.satisfied = True
                    else:
                        req.next += 1
                    lib.curr_creds += int(c.creds)
                    self.total_creds += int(c.creds)

    def read_cs(self):
        for cat in self.requirements:
            if cat.cat_name == "Computer Science":
                cs = cat
                break
        for req in cs.reqs:
            if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                self.ppf[ppf_creds_col + str(req.position)] = None
                self.ppf[ppf_grade_col + str(req.position)] = None
            elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                c = read_class_from_ppf(self.ppf, req.position)
                req.course = c
                req.satisfied = True
                cs.curr_creds += int(c.creds)
                self.total_creds += int(c.creds)

    def read_eng(self):
        for cat in self.requirements:
            if cat.cat_name == "Engineering Requirements":
                eng = cat
                break
        for req in eng.reqs:
            if isinstance(req, BasicCourseReq):
                if is_semester(self.ppf[ppf_grade_col + str(req.position)].value):
                    self.ppf[ppf_creds_col + str(req.position)] = None
                    self.ppf[ppf_grade_col + str(req.position)] = None
                elif self.ppf[ppf_creds_col + str(req.position)].value is not None:
                    c = read_class_from_ppf(self.ppf, req.position)
                    req.course = c
                    req.satisfied = True
                    eng.curr_creds += int(c.creds)
                    self.total_creds += int(c.creds)
            elif isinstance(req, MultiCourseReq):
                for p in req.positions:
                    if is_semester(self.ppf[ppf_grade_col + str(p)].value):
                        self.ppf[ppf_creds_col + str(p)] = None
                        self.ppf[ppf_grade_col + str(p)] = None
                    elif self.ppf[ppf_creds_col + str(p)].value is not None:
                        c = read_class_from_ppf(self.ppf, p)
                        if req.courses is None:
                            req.courses = [c]
                        else:
                            req.courses.append(c)
                        req.creds_taken += int(c.creds)
                        if req.creds_taken >= req.creds_needed:
                            req.satisfied = True
                        else:
                            req.next += 1
                        eng.curr_creds += int(c.creds)
                        self.total_creds += int(c.creds)

    def read_approved(self):
        for cat in self.requirements:
            if cat.cat_name == "Approved Electives":
                approved = cat.reqs[0]
                break

        while self.ppf[ppf_creds_col+str(approved.next)].value is not None:
            c = read_class_from_ppf(self.ppf, approved.next)
            if approved.courses is None:
                approved.courses = [c]
            else:
                approved.courses.append(c)
            approved.creds += c.creds
            approved.next += 1

    def read_others(self):
        while self.ppf[ppf_courses_unneeded_col+str(self.notneeded_next)].value is not None:
            self.notneeded_next += 1

    def update_ppf(self):
        # Delete the old summary
        p = 111
        while self.ppf['K'+str(p)].value is not None:
            self.ppf['K'+str(p)] = None
            p += 1

        # Update
        for cat in self.requirements:
            if cat.cat_name == "Math" and cat.satisfied is False:
                self.update_math()
            if cat.cat_name == "Chemistry" and cat.satisfied is False:
                self.update_chem()
            if cat.cat_name == "Physics" and cat.satisfied is False:
                self.update_phys()
            if cat.cat_name == "Biological Sciences" and cat.satisfied is False:
                self.update_bio()
            if cat.cat_name == "First-Year Writing Seminar" and cat.satisfied is False:
                self.update_fws()
            if cat.cat_name == "Liberal Studies" and cat.satisfied is False:
                self.update_lib()
            if cat.cat_name == "Computer Science" and cat.satisfied is False:
                self.update_cs()
            if cat.cat_name == "Engineering Requirements" and cat.satisfied is False:
                self.update_eng()

        self.update_approved_electives()
        self.ppf[ppf_grand_total] = self.total_creds

        # Save the updates that have been made
        parent = os.getcwd()
        os.chdir(parent+self.folder)
        self.wb.save(self.filename)
        os.chdir(parent)

    def update_math(self):

        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Math":
                math = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in math.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course and update ppf
                        self.course_list.remove(c)
                        math.curr_creds += c.creds
                        self.total_creds += int(c.creds)
                        break

        # update the total number of credits taken
        self.ppf[math.loc] = math.curr_creds
        if math.curr_creds >= math.min_creds:
            math.satisfied = True

    def update_phys(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Physics":
                phys = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in phys.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        self.course_list.remove(c)
                        phys.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[phys.loc] = phys.curr_creds
        if phys.curr_creds >= phys.min_creds:
            phys.satisfied = True

    def update_chem(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Chemistry":
                chem = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in chem.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        self.course_list.remove(c)
                        chem.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[chem.loc] = chem.curr_creds
        if chem.curr_creds >= chem.min_creds:
            chem.satisfied = True

    def update_bio(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Biological Sciences":
                bio = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in bio.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        self.course_list.remove(c)
                        bio.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[bio.loc] = bio.curr_creds
        if bio.curr_creds >= bio.min_creds:
            bio.satisfied = True

    def update_fws(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "First-Year Writing Seminar":
                fws = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in fws.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    is_fws = "FWS" in c.desc or c.num == "ENGL2880" or c.num == "ENGL2890"
                    if is_fws and r.check_fillby(c, override=True):
                        r.fillby(c, ppf=self.ppf, override=True, include_desc=True)  # save the course
                        self.course_list.remove(c)
                        fws.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

    def update_lib(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Liberal Studies":
                lib = cat
                break

        for r in lib.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)

    def update_cs(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Computer Science":
                cs = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in cs.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        self.course_list.remove(c)
                        cs.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[cs.loc] = cs.curr_creds
        if cs.curr_creds >= cs.min_creds:
            cs.satisfied = True

    def update_eng(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Engineering Requirements":
                eng = cat
                break

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in eng.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        self.course_list.remove(c)
                        eng.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[eng.loc] = eng.curr_creds
        if eng.curr_creds >= eng.min_creds:
            eng.satisfied = True

    def update_approved_electives(self):
        for cat in self.requirements:
            if cat.cat_name == "Approved Electives":
                approved = cat.reqs[0]
                break

        for c in self.course_list:
            # Go through unused courses - if they can satisfy approved, apply it, otherwise put it in unused
            failing_grades = ['U', 'UX', 'W', 'INC', 'NGR', 'F']
            if failing_grades.__contains__(c.grade):
                pass
                # TODO
            else:
                if approved.check_fillby(c):
                    approved.fillby(c, self.ppf)
                else:
                    self.ppf[ppf_courses_unneeded_col+str(self.notneeded_next)] = c.num
                    self.notneeded_next += 1

    def write_summary(self):
        # PPF Summary
        self.ppf['K111'] = "The following courses are needed for graduation:"
        row = 112
        for cat in self.requirements:
            for r in cat.reqs:
                if isinstance(r, BasicCourseReq) and r.satisfied is False:
                    if len(r.options) == 1:
                        self.ppf['K'+str(row)] = r.options[0]
                        row += 1
                    elif len(r.options) == 2:
                        self.ppf['K'+str(row)] = r.options[0] + " or " + r.options[1]
                        row += 1
                    else:
                        self.ppf['K'+str(row)] = r.req_name
                elif isinstance(r, MultiCourseReq) and r.satisfied is False:
                    self.ppf['K'+str(row)] = r.req_name + " (%d more credits)" % (r.creds_needed-r.creds_taken)
                    row += 1

        # Save the updates that have been made
        parent = os.getcwd()
        os.chdir(parent + self.folder)
        self.wb.save(self.filename)
        os.chdir(parent)

