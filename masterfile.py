from helper_tools import *
from Student import Student


def main():

    # In testing mode, will use transcript_test.xlsx and will write to the Students_test
    # folder.  Otherwise, will use transcript.xlsx and write to the Students folder
    test = True
    if test:
        _, _, transcript = open_excel_file("transcript_test.xlsx")
    else:
        _, _, transcript = open_excel_file("transcript.xlsx")

    cols = designate_columns(transcript)  # Record what is in each column of transcript
    row = '2'  # Begin reading from first non-title row
    students_remain = True
    student_courses_remain = True

    summary = open("summary.txt", "w")

    while students_remain:
        curr = Student(transcript, row, cols, test)
        summary.write("%s\n \n" % curr.name)
        while student_courses_remain:
            c = read_class_from_transcript(transcript, cols, row)
            curr.course_list.append(c)
            row = str(int(row) + 1)
            if transcript[cols['student name'] + row].value is None:
                students_remain = False
                break
            elif transcript[cols['student name'] + row].value != curr.name:
                break
        curr.update_ppf()
        curr.update_summary(summary)
        summary.write("\n \n")
    summary.close()


if __name__ == "__main__":
    main()
