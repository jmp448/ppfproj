from support_files.helper_tools import *
from support_files.Student import Student
from support_files.web_reader import *


def main():

    # Make sure the transcript file is in place
    print("Current directory: %s\n" % os.getcwd())
    print("Contents of current directory: %s\n" % os.listdir("."))
    print("Contents of Transcript folder: %s\n" % os.listdir("./Transcript"))

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

    # Will use transcript.xlsx and write to the Students folder
    file, first_transcript, num_transcripts = open_transcript_file("./Transcript/transcript.xlsx")

    transcript_index = first_transcript
    for _ in range(num_transcripts):
        file.active = transcript_index
        transcript = file.active
        cols = designate_columns(transcript)  # Record what is in each column of transcript
        row = '2'  # Begin reading from first non-title row
        students_remain = True
        student_courses_remain = True

        # Create summary file for Brenda
        brenda_summary = open("./Students/summary.txt", "a")

        while students_remain:
            curr = Student(transcript, row, cols)
            brenda_summary.write("\n%s\n" % curr.name)
            if curr.grad == "N/A":
                print("No PPF created for %s, grad term listed as N/A" % curr.name)
                continue
            while student_courses_remain:
                c = read_class_from_transcript(transcript, cols, row)
                if c is not None:
                    if isinstance(c, str):
                        curr.brenda_summary_notes.append("Transfer course taken: %s" % c)
                    elif isinstance(c, list):
                        for course in c:
                            curr.course_list.append(course)
                    else:
                        curr.course_list.append(c)
                row = str(int(row) + 1)
                if transcript[cols['student name'] + row].value is None:
                    students_remain = False
                    break
                elif transcript[cols['student name'] + row].value != curr.name:
                    break
            # Sort student course list so that regular courses appear first, then AP courses, then upcoming courses
            i = 0  # AP courses shoved to the end
            end = len(curr.course_list)
            while i < end:
                c = curr.course_list[i]
                if c.ap:
                    curr.course_list.append(curr.course_list.pop(i))
                    end -= 1
                else:
                    i += 1
            i = 0  # now the upcoming courses shoved to the end, even after the APs
            while i < end:
                c = curr.course_list[i]
                if c.grade is None and not c.ap:
                    curr.course_list.append(curr.course_list.pop(i))
                    end -= 1
                else:
                    i += 1
            curr.update_ppf()

            # Write Brenda's summary file
            for comment in curr.brenda_summary_notes:
                brenda_summary.write(comment + "\n")

            if summary_sems.__contains__(curr.grad):
                curr.write_summary(write_reqs_remaining=True)
            else:
                curr.write_summary(write_reqs_remaining=False)

        brenda_summary.close()
        transcript_index += 1


if __name__ == "__main__":
    main()
