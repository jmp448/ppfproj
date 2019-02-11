from openpyxl import load_workbook
from helper_tools import *
from helper_structs import *
import os


PPF_COLS = {
    'Course': 'G',
    'Grade': 'I',
    'Credits': 'K',
    'Totals': 'M'
}


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


def test_read_class_ppf():
    parent = os.getcwd()
    os.chdir(parent + "/Students_test")

    ppf = open_excel_file("poppj-jmp448.xlsx")
    c = read_class_from_ppf(ppf, 12)
    assert(c.num == 'MATH 1910')
    assert(c.creds == 4)
    assert(c.grade == 'A+')

    os.chdir(parent)

    print('read_class_from_ppf is working')



def main():
    # test_read_class_ppf()
    _, _, transcript = open_excel_file("transcript_test.xlsx")

    cols = designate_columns(transcript)
    row = '2'

    students_remain = True
    on_current_student = True

    while students_remain:
        curr = Student(transcript, row, cols)
        while on_current_student:
            c = read_class_from_transcript(transcript, cols, row)
            curr.courses_unused.append(c)
            curr.courses_taken.append(c)
            row = str(int(row) + 1)
            if transcript[cols['student name'] + row].value is None:
                students_remain = False
                break
            elif transcript[cols['student name'] + row].value != curr.name:
                break

        curr.update_ppf()
        # curr.check_1200()
        # curr.check_pe()
        # curr.check_capstone()




if __name__ == "__main__":
    main()
