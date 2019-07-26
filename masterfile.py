from support_files.helper_tools import *
from support_files.Student import Student
from support_files.web_reader import *


def main():

    # Ask user if they want to refresh liberal arts and focus area courses
    refresh_lib = input("Would you like to refresh the liberal arts course listings from online?  Yes or No\n")
    if refresh_lib == "Yes":
        refresh_libarts_all()
    refresh_fa = input("Would you like to refresh the focus area course listings from online?  Yes or No\n")
    if refresh_fa == "Yes":
        refresh_focus_areas()

    # Prompt user for what grad sems they want included in
    summary_sems_str = input("Whose info would you like included in the summary?\nList in the same form they appear on the transcript, separated by a comma without spaces\nFor example: Fall 2018,Spring 2019\n\n")
    summary_sems = summary_sems_str.split(",")

    # In testing mode, will use transcript_test.xlsx and will write to the Students_test
    # folder.  Otherwise, will use transcript.xlsx and write to the Students folder
    test = True
    parent = os.getcwd()
    os.chdir(parent + "/Transcript")
    if test:
        _, _, transcript = open_excel_file("test.xlsx")
        # _, _, transcript = open_excel_file("PoppJoshua_UnofficialTranscriptForPPFProject_6_19_18.xlsx")
    else:
        _, _, transcript = open_excel_file("transcript.xlsx")
    os.chdir(parent)

    cols = designate_columns(transcript)  # Record what is in each column of transcript
    row = '2'  # Begin reading from first non-title row
    students_remain = True
    student_courses_remain = True

    while students_remain:
        curr = Student(transcript, row, cols, test)
        if curr.grad == "N/A":
            print("No PPF created for %s, grad term listed as N/A" % curr.name)
            break
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
        if summary_sems.__contains__(curr.grad):
            curr.write_summary()


if __name__ == "__main__":
    main()
