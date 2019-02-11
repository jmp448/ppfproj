import os
from helper_tools import *
from shutil import copyfile

'''
Create objects used to store PPF data
'''


class Course:

    def __init__(self, num, grade, creds, term=None, desc=None):
        self.num = num
        self.grade = grade
        self.creds = creds
        self.term = term
        self.desc = desc


class CourseReq:

    def __init__(self, req_name, opts, taken=False, course=None, creds=None, position=None):
        self.req_name = req_name
        self.taken = taken
        self.course = course
        self.creds = creds
        self.opts = opts
        self.position = position

    def fillby(self, course):
        self.taken = True
        self.course = course


reqs_list = [
    CourseReq('Calc I', ['MATH1910'], position=12),
    CourseReq('Calc II', ['MATH1920'], position=13),
    CourseReq('Diff Eq', ['MATH2930'], position=14),
    CourseReq('Lin Alg', ['MATH2940'], position=15),
    CourseReq('Mechanics', ['PHYS1112'], position=19),
    CourseReq('Electromagnetism', ['PHYS2213'], position=20),
    CourseReq('Gen Chem', ['CHEM2070', 'CHEM2090'], position=23),
    CourseReq('Orgo', ['CHEM1570', 'CHEM3530', 'CHEM3570'], position=24),
    CourseReq('Bio Lab', ['BIOG1500'], position=29),
    CourseReq('Computer Science', ['BEE1510', 'CS1112'], position=65),
    CourseReq('Statics', ['ENGRD2020'], position=70),
    CourseReq('Statistics', ['CEE3040', 'ENGRD2700'], position=71),
    CourseReq('Intro Engineering', ['BEE1200'], position=73),
    CourseReq('Thermodynamics', ['BEE2220', 'ENGRD2210', 'CHEME3130', 'MSE3030'], position=74),
    CourseReq('Engineering Distribution', ['BEE2600', 'BEE2510'], position=76),
    CourseReq('Fluid Mechanics', ['BEE3310'], position=77),
    CourseReq('Biomaterials', ['BEE3400'], position=78),
    CourseReq('Heat and Mass', ['BEE3500'], position=79),
    CourseReq('Molecular and Cellular Bioengineering', ['BEE3600'], position=80),
    CourseReq('Bioinstrumentation', ['BEE4500'], position=81)
]


def read_class_from_ppf(ppf, row):
    if isinstance(row, int):
        row = str(row)

    course_loc = PPF_COLS['Course'] + row
    course = ppf[course_loc].value

    grade_loc = PPF_COLS['Grade'] + row
    grade = ppf[grade_loc].value

    creds_loc = PPF_COLS['Credits'] + row
    creds = ppf[creds_loc].value

    c = Course(course, grade, creds)

    return c


class Student:
    def __init__(self, transcript, row, cols):
        name_loc = cols['student name'] + row
        self.name = transcript[name_loc].value

        netid_loc = cols['netid'] + row
        self.netid = transcript[netid_loc].value

        studid_loc = cols['student id'] + row
        self.student_id = transcript[studid_loc].value

        grad_loc = cols['grad'] + row
        self.grad = transcript[grad_loc].value

        # advisor_loc = cols['advisor'] + row
        # self.advisor = transcript[advisor_loc].value

        self.courses_taken = []
        self.courses_used = []
        self.courses_unused = []
        self.unsatisfied_reqs = reqs_list
        self.satisfied_reqs = []

        self.pe = 0
        self.capstone = False
        self.intro_bee = False

        # Check to see if student has a ppf
        parent = os.getcwd()
        os.chdir(parent + "/Students_test")  ## TODO: update later

        [lname, fname] = self.name.split(',')
        filename = lname.lower() + fname[0].lower() +\
                   '-' + self.netid + '.xlsx'

        if os.path.isfile(filename):
            self.filename, self.wb, self.ppf = open_excel_file(filename)
            os.chdir(parent)
        else:
            self.create_ppf()
            os.chdir(parent)


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
        assert(self.has_ppf)
        reqs_dict = {req.position: req for req in self.unsatisfied_reqs}

        for pos in reqs_dict.keys():
            if self.ppf['K'+str(pos)] is not None:
                c = read_class_from_ppf(self.ppf, pos)
                self.courses_taken.append(c)
                req = reqs_dict[pos]
                self.unsatisfied_reqs.remove(req)
                req.fillby(c)
                self.satisfied_reqs.append(req)


    def update_ppf(self):
        parent = os.getcwd()
        os.chdir(parent + "/Students_test")
        for r in self.unsatisfied_reqs:
            for c in self.courses_unused:
                if r.opts.__contains__(c.num):
                    r.fillby(c)
                    self.satisfied_reqs.append(r)
                    self.unsatisfied_reqs.remove(r)
                    self.courses_unused.remove(c)
                    self.courses_used.append(c)

                    self.ppf['G'+str(r.position)] = c.num
                    self.ppf['I'+str(r.position)] = c.grade
                    self.ppf['K'+str(r.position)] = c.creds

                    if r.req_name == "Thermodynamics":
                        self.ppf['G75'] = None

        self.wb.save(filename=self.filename)
        self.fill_totals()

        os.chdir(parent)


    def check_capstone(self):
        capstones = ["BEE4350", "BEE4500", "BEE4530", "BEE4600", "BEE4730", "BEE4870"]
        #TODO Handle BEE 4500 (3/4 credit) and BEE 4810/4960
        for c in capstones:
            if self.courses_taken.__contains__(c):
                self.capstone = True

    def check_pe(self):
        num_taken = 0
        while num_taken < 2:
            for c in self.courses_taken:
                if c.dept == "PE":
                    num_taken += 1
            break

        self.pe = num_taken

    def check_1200(self):
        for c in self.courses_taken:
            if c.course_num == "BEE1200":
                self.intro_bee = True

    def fill_totals(self):

        math = ['K12', 'K13', 'K14', 'K15']
        math_tot = 0
        for c in math:
            if self.ppf[c].value is not None:
                math_tot += int(self.ppf[c].value)
        self.ppf['M15'] = math_tot

        physics = ['K19', 'K20']
        physics_tot = 0
        for c in physics:
            if self.ppf[c].value is not None:
                physics_tot += int(self.ppf[c].value)
        self.ppf['M20'] = physics_tot

        chem = ['K23', 'K24']
        chem_tot = 0
        for c in chem:
            if self.ppf[c].value is not None:
                chem_tot += int(self.ppf[c].value)
        self.ppf['M24'] = chem_tot

        bio = ['K27', 'K28', 'K29', 'K30', 'K32']
        bio_tot = 0
        for c in bio:
            if self.ppf[c].value is not None:
                bio_tot += int(self.ppf[c].value)
        self.ppf['M32'] = bio_tot

        writing = ['K35', 'K36']
        writing_tot = 0
        for c in writing:
            if self.ppf[c].value is not None:
                writing_tot += int(self.ppf[c].value)
        self.ppf['M36'] = writing_tot

        libs = ['K49', 'K50', 'K51', 'K52', 'K53', 'K54']
        libs_tot = 0
        for c in libs:
            if self.ppf[c].value is not None:
                libs_tot += int(self.ppf[c].value)
        self.ppf['M57'] = libs_tot

        cs = ['K65']
        cs_tot = 0
        if self.ppf['K65'].value is not None:
            cs_tot = int(self.ppf['K65'].value)
        self.ppf['M65'] = cs_tot

        eng = ['K70', 'K71', 'K73', 'K74', 'K76',
               'K77', 'K78', 'K79', 'K80', 'K81',
               'K84', 'K85', 'K86', 'K87', 'K88']
        eng_tot = 0
        for c in eng:
            if self.ppf[c].value is not None:
                eng_tot += int(self.ppf[c].value)
        self.ppf['M90'] = eng_tot

        approved = ['K92', 'K93', 'K94', 'K95']
        app_tot = 0
        for c in approved:
            if self.ppf[c].value is not None:
                app_tot += int(self.ppf[c].value)
        self.ppf['M95'] = app_tot

        grand = sum([math_tot, physics_tot, chem_tot,
                    bio_tot, writing_tot, libs_tot, cs_tot,
                    eng_tot, app_tot])
        self.ppf['M98'] = grand

        self.wb.save(filename=self.filename)


    def list_progress(self):
        for r in self.satisfied_reqs:
            print("%s satisfied by %s" % (r.req_name, r.course.num))
        for r in self.unsatisfied_reqs:
            print("%s unsatisfied" % r.req_name)

        os.chdir(parent)
