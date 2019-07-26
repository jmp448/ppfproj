from openpyxl import load_workbook
from support_files.Course import Course
import xlrd
import numpy as np

PPF_COLS = {
    'Course': 'G',
    'Grade': 'I',
    'Credits': 'K',
    'Totals': 'M'
}


# Create column hopping function
def colhop(curr, steps=1):

    curr_col = curr[0]
    curr_row = curr[1:]

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    loc = 0
    while letters[loc] != curr_col:
        loc += 1
        if loc == len(letters):
            print('Error with column hopping')

    final_pos = loc + steps
    if final_pos < 0 or final_pos >= len(letters):
        print('Error with column hopping')
    else:
        return letters[final_pos] + str(curr_row)


# Create row hopping function
def rowhop(curr, steps=1):
    curr_col = curr[0]
    curr_row = curr[1:]

    dest = int(curr_row) + steps

    if dest <= 0:
        print('Error with row hopping')
    else:
        return curr_col + str(dest)


def exceeds(a, threshold='C-'):

    grades = {
        'A+': 4.3,
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }

    #TODO fix
    if "*" in a:
        a = a[:-1]
    assert grades.keys().__contains__(a), "Cannot compare a non-letter grade (%s) to the letter grade threshold (%s)" % (a, threshold)
    if grades[a] >= grades[threshold]:
        return True
    else:
        return False


def designate_columns(transcript):
    pos = 'A1'
    curr = transcript[pos].value
    cols = {}

    while curr is not None:
        if curr == 'Academic Term Ldescr' or curr == 'Academic Term Sdescr':
            cols['semester'] = pos[0]
        elif curr == 'Effdt Primary Name' or curr == 'Effdt Preferred Name':
            cols['student name'] = pos[0]
        elif curr == 'Netid':
            cols['netid'] = pos[0]
        elif curr == 'Employee Id':
            cols['student id'] = pos[0]
        elif curr == 'Advisor':
            cols['advisor'] = pos[0]
        elif curr == 'Exp Grad Term Ldescr' or curr == 'Exp Grad Term Sdescr':
            cols['grad'] = pos[0]
        elif curr == 'Class Descr':
            cols['desc'] = pos[0]
        elif curr == 'Subject':
            cols['dept'] = pos[0]
        elif curr == 'Catalog Nbr':
            cols['num'] = pos[0]
        elif curr == 'Official Grade':
            cols['grade'] = pos[0]
        elif curr == 'Unt Taken':
            cols['creds'] = pos[0]

        pos = colhop(pos)
        curr = transcript[pos].value

    return cols


def open_excel_file(filename):

    wb = load_workbook(filename=filename, data_only=True)
    file = wb.active

    return filename, wb, file


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

    # TODO AP classes stored differently
    # TODO courses taken next semester stored differently

    return c


def read_class_from_transcript(transcript, cols, row):

    dept_loc = cols['dept'] + row
    dept = transcript[dept_loc].value

    num_loc = cols['num'] + row
    num = transcript[num_loc].value

    course_num = dept + str(num)

    creds_loc = cols['creds'] + row
    creds = transcript[creds_loc].value

    grade_loc = cols['grade'] + row
    grade = transcript[grade_loc].value

    desc_loc = cols['desc'] + row
    desc = transcript[desc_loc].value

    term_loc = cols['semester'] + row
    term = transcript[term_loc].value

    c = Course(course_num, grade, creds, term=term, desc=desc)

    if c.desc == 'AP':
        c.grade = 'AP'
    if c.desc == 'LEC':
        c.grade = c.term

    return c


def upload_adv_bio():

    courses = []
    wb = xlrd.open_workbook("advanced_bio.xlsx")
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        courses.append(sheet.cell_value(i, 0))
    return courses


def is_semester(s):
    if s is None:
        return True
    else:
        return any(c.isdigit() for c in s)


def categories_represented(courses):
    total_cats = []
    for c in courses:
        for cat in c.categories:
            if total_cats.__contains__(cat) is False:
                total_cats.append(cat)
    table = np.zeros([len(courses), len(total_cats)], dtype=bool)
    for c in courses:
        for l in total_cats:
            if c.categories.__contains__(l):
                table[courses.index(c)][total_cats.index(l)] = 1
    tot = 0
    for c in range(len(courses)):
        if sum(table[c][:]) >= 1:
            tot += 1
    return tot


def sdescr2ldescr(s):
    assert " " in s is False, "Is this really a short description? %s\n" % s
    year = s[0:4]
    sem = s[4:]

    if sem == "FA":
        return "Fall " + year
    elif sem == "SP":
        return "Spring " + year
    else:
        print("%s is not an expected sdescr (XXXXFA or XXXXSP)" % s)


def ldescr2sdescr(s):
    assert " " in s, "Is this really a long description? %s\n" % s
    [sem, year] = s.split()

    if sem == "Fall":
        return year + "FA"
    elif sem == "Spring":
        return year + "SP"
    else:
        print("%s is not an expected ldescr (Fall XXXX or Spring XXXX)" % s)
