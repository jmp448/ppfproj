from define_reqs import category_list
from helper_tools import *
from shutil import copyfile
from ReqTypes import BasicCourseReq,  MultiCourseReq
import os

ppf_creds_col = 'K'
ppf_grade_col = 'I'
ppf_course_col = 'G'
ppf_grand_total = 'M98'


class Student:
    def __init__(self, transcript, row, cols, test=False, course_list=None):
        name_loc = cols['student name'] + row
        self.name = transcript[name_loc].value

        netid_loc = cols['netid'] + row
        self.netid = transcript[netid_loc].value

        studid_loc = cols['student id'] + row
        self.student_id = transcript[studid_loc].value

        grad_loc = cols['grad'] + row
        self.grad = transcript[grad_loc].value

        self.requirements = category_list

        self.test = test

        self.total_creds = 0

        if course_list is None:
            self.course_list = []
        else:
            self.course_list = course_list

        # Check to see if student has a ppf
        parent = os.getcwd()
        has_ppf, filename = self.has_ppf()
        if has_ppf:  # if they do have a PPF, read it
            if self.test:
                os.chdir(parent + "/Students_test")
            else:
                os.chdir(parent + "/Students")
            self.filename, self.wb, self.ppf = open_excel_file(filename)
            os.chdir(parent)
            self.read_ppf()
        else:  # if they don't, create a new one
            self.create_ppf()
            os.chdir(parent)

    def has_ppf(self):
        parent = os.getcwd()
        os.chdir(parent + "/Students_test")  # TODO: update later

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
        folder = os.getcwd()
        template = folder + '/blankPPF.xlsx'

        [lname, fname] = self.name.split(',')
        file = '/' + lname.lower() + fname[0].lower() + '-' + self.netid + '.xlsx'

        file = folder + file

        copyfile(template, file)

        self.filename, self.wb, self.ppf = open_excel_file(file)

        # Fill student info
        self.ppf['B5'] = self.name
        self.ppf['B6'] = self.netid
        self.ppf['G6'] = self.student_id
        # ppf['L6'] = student.advisor
        self.ppf['M7'] = self.grad

        self.wb.save(filename=self.filename)

    def read_ppf(self):

        assert self.has_ppf(), "%s does not have a PPF yet" % self.name

        for cat in self.requirements:
            for req in cat.reqs:
                if isinstance(req, BasicCourseReq):
                    if self.ppf[ppf_creds_col+str(req.position)].value is not None:
                        c = read_class_from_ppf(self.ppf, req.position)
                        req.course = c
                        req.satisfied = True
                        # NOTE that this is hard-coded, there is no system for checking the ppf is correct
                        self.total_creds += int(c.creds)
                elif isinstance(req, MultiCourseReq):
                    for p in req.positions:
                        if self.ppf[ppf_creds_col+str(p)].value is not None:
                            c = read_class_from_ppf(self.ppf, p)
                            req.courses.append(c)
                            req.creds_taken += int(c.creds)
                            if req.creds_taken >= req.creds_needed:
                                req.satisfied = True
                            else:
                                req.next += 1
                            self.total_creds += int(c.creds)
            cat.update_total()

    def update_ppf(self):
        for cat in self.requirements:
            if cat.cat_name == "Math" and cat.satisfied is False:
                self.update_math()
            if cat.cat_name == "Chemistry" and cat.satisfied is False:
                self.update_chem()
            if cat.cat_name == "Physics" and cat.satisfied is False:
                self.update_phys()
            if cat.cat_name == "Biological Sciences" and cat.satisfied is False:
                self.update_bio()
            if cat.cat_name == "Computer Science" and cat.satisfied is False:
                self.update_cs()
            if cat.cat_name == "Engineering Requirements" and cat.satisfied is False:
                self.update_eng()

        self.ppf[ppf_grand_total] = self.total_creds

        # Save the updates that have been made
        parent = os.getcwd()
        if self.test:
            os.chdir(parent+"/Students_test")
        else:
            os.chdir(parent+"/Students")
        self.wb.save(self.filename)
        os.chdir(parent)

        # TODO the rest of the update types
        # TODO AP credit

    def update_math(self):

        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Math":
                math = cat

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in math.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course and update ppf
                        math.curr_creds += c.creds
                        self.total_creds += int(c.creds)
                        break

        # update the total number of credits taken
        self.ppf[math.loc] = math.curr_creds
        if math.curr_creds >= math.min_creds:
            math.satisfied = True

        # TODO check grade thresholds

    def update_phys(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Physics":
                phys = cat

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in phys.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
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

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in chem.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
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

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in bio.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        bio.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[bio.loc] = bio.curr_creds
        if bio.curr_creds >= bio.min_creds:
            bio.satisfied = True

    def update_fws(self):
        pass
        #TODO

    def update_lib(self):
        pass
        #TODO

    def update_cs(self):
        for cat in self.requirements:
            # get the student's current info
            if cat.cat_name == "Computer Science":
                cs = cat

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in cs.reqs:
            if r.satisfied is False:
                for c in self.course_list:
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
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

        # look through the unsatisfied reqs
        # see if any can be satisfied by a course the student took
        for r in eng.reqs:
            classes_remaining = len(self.course_list)
            while r.satisfied is False and classes_remaining > 0:
                for c in self.course_list:
                    classes_remaining -= 1
                    if r.check_fillby(c):
                        r.fillby(c, self.ppf)  # save the course
                        eng.curr_creds += c.creds
                        self.total_creds += c.creds
                        break

        # update the total number of credits taken
        self.ppf[eng.loc] = eng.curr_creds
        if eng.curr_creds >= eng.min_creds:
            eng.satisfied = True

    def update_summary(self, summary):
        for cat in self.requirements:
            if cat.satisfied is False:
                summary.write("%d credits left in %s\n" % (cat.min_creds-cat.curr_creds, cat.cat_name))
