from openpyxl import load_workbook
from Course import Course

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

    if a == 'AP' or a[0:2] == '20':
        return True
    elif grades[a] >= grades[threshold]:
        return True
    else:
        return False


def designate_columns(transcript):
    pos = 'A1'
    curr = transcript[pos].value
    cols = {}

    while curr is not None:
        if curr == 'Academic Term Ldescr':
            cols['semester'] = pos[0]
        elif curr == 'Effdt Primary Name':
            cols['student name'] = pos[0]
        elif curr == 'Netid':
            cols['netid'] = pos[0]
        elif curr == 'Employee Id':
            cols['student id'] = pos[0]
        elif curr == 'Advisor':
            cols['advisor'] = pos[0]
        elif curr == 'Exp Grad Term Ldescr':
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
