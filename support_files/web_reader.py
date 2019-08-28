import requests
import re
import os
from support_files.helper_tools import open_excel_file, upload_courses_from_file


"""
URL and filenames, for directory navigation
"""

fa_url = 'http://beadvised.bee.cornell.edu/full-list-of-focus-area-courses-fall-2018-and-later/'
ca_url = 'https://apps.engineering.cornell.edu/liberalstudies/CA.cfm'
ha_url = 'https://apps.engineering.cornell.edu/liberalstudies/HA.cfm'
kcm_url = 'https://apps.engineering.cornell.edu/liberalstudies/KCM.cfm'
la_url = 'https://apps.engineering.cornell.edu/liberalstudies/LA.cfm'
sba_url = 'https://apps.engineering.cornell.edu/liberalstudies/SBA.cfm'
ce_url = 'https://apps.engineering.cornell.edu/liberalstudies/CE.cfm'

fa_file = "focus_area_raw_code.txt"
ca_file = "ca_raw_code.txt"
ha_file = "ha_raw_code.txt"
kcm_file = "kcm_raw_code.txt"
la_file = "la_raw_code.txt"
sba_file = "sba_raw_code.txt"
ce_file = "ce_raw_code.txt"

libarts_files = [ca_file, ha_file, kcm_file, la_file, sba_file, ce_file]


"""Support methods"""


def refresh_focus_areas():
    """
    This creates a text file containing the source code for the BEE focus area course listings found at fa_url
    """

    parent = os.getcwd()
    os.chdir(parent + "/support_files/website_data")

    r = requests.get(fa_url)
    fa_code = open(fa_file, "w")
    fa_code.write(r.text)
    fa_code.close()

    os.chdir(parent)


def refresh_libarts_all():

    parent = os.getcwd()
    os.chdir(parent+"/support_files/website_data")

    refresh_libarts_ca()
    refresh_libarts_ce()
    refresh_libarts_ha()
    refresh_libarts_kcm()
    refresh_libarts_sba()
    refresh_libarts_la()

    os.chdir(parent)


def refresh_libarts_ca():

    r = requests.get(ca_url)
    ca_code = open(ca_file, "w")
    ca_code.write(r.text)
    ca_code.close()


def refresh_libarts_ha():

    r = requests.get(ha_url)
    ha_code = open("ha_raw_code.txt", "w")
    ha_code.write(r.text)
    ha_code.close()


def refresh_libarts_kcm():

    r = requests.get(kcm_url)
    kcm_code = open(kcm_file, "w")
    kcm_code.write(r.text)
    kcm_code.close()


def refresh_libarts_la():

    r = requests.get(la_url)
    la_code = open(la_file, "w")
    la_code.write(r.text)
    la_code.close()


def refresh_libarts_sba():

    r = requests.get(sba_url)
    sba_code = open(sba_file, "w")
    sba_code.write(r.text)
    sba_code.close()


def refresh_libarts_ce():

    r = requests.get(ce_url)
    ce_code = open(ce_file, "w")
    ce_code.write(r.text)
    ce_code.close()


def get_category_list(filename):
    """
    Returns a list of course numbers in the format [AAS1100, SPAN3040, ...] from an HTML file on the liberal studies site
        (these courses will be from a single category: CA OR HA etc since these are stored on different pages)

    This uses the criteria of having two consecutive </td><td> to figure out where the courses are
    """
    course_list = []
    f = open(filename, "r")
    for l in f:
        if "</td><td>" in l:
            l = l.replace("<td>", " ")
            l = l.replace("</td>", " ")
            l = l.split()
            assert len(l) == 2, "Picked up the wrong info from a liberal arts course listing"
            c = l[0] + l[1]
            course_list.append(c)

    return course_list


def add_other_yes(dic):
    parent = os.getcwd()
    os.chdir(parent + "/support_files")
    _, _, other_yes = open_excel_file("other_yes.xlsx")

    dept_col = 'A'
    num_col = 'B'
    category_col = 'E'
    notes_col = 'I'

    # Read through the other_yes file
    row = 7
    while other_yes[dept_col + str(row)].value is not None:
        comments = other_yes[notes_col + str(row)].value

        """
        read the comments for each course list to get all cross-listed courses or former course listings, and eliminate
        courses with footnotes indicating that they must be petitioned or are no longer accepted
        """
        if comments is None:
            courses = [other_yes[dept_col+str(row)].value + str(other_yes[num_col+str(row)].value)]

        # do not include courses that say they will need to be petitioned
        elif "petition" in comments or "petitioned" in comments:
            row += 1
            continue

        # do not include courses that are only permitted for certain semesters
        elif "nly permitted if taken" in comments:
            row += 1
            continue

        # for crosslisted courses, create separate items for each cross-listing of the course
        elif comments[:5] == "Also ":
            if "(" in comments:
                stop = comments.index("(")
                comments = comments[5:stop]
            else:
                comments = comments[5:]
            comments = comments.replace(", and ", ", ")  # to avoid ending up with ,, in case of Oxford comma
            comments = comments.replace(" and ", ", ")
            comments = comments.replace(" ", "")
            courses = comments.split(",")
            courses.append(other_yes[dept_col+str(row)].value + str(other_yes[num_col+str(row)].value))

        # individual case for one tough comment - "Formerly Interior Design Studio I; Also VISST 1101 (crosslisted)"
        elif comments == "Formerly Interior Design Studio I; Also VISST 1101 (crosslisted)":
            courses = ['VISST1101', 'DEA1101']

        # for courses formerly listed as something else, create separate listings for each possible listing
        elif comments[:9] == "Formerly ":
            comments = comments[9:]
            comments = comments.replace(" ", "")
            courses = [comments]
            courses.append(other_yes[dept_col+str(row)].value + str(other_yes[num_col+str(row)].value))

        # all other comments are ignored (treated same as no comments)
        else:
            courses = [other_yes[dept_col + str(row)].value + str(other_yes[num_col + str(row)].value)]

        # Read categories from category column
        categories = other_yes[category_col + str(row)].value
        categories = categories.replace("or", ",")
        categories = categories.replace(" ", "")
        categories = categories.split(",")

        for c in courses:
            if dic.keys().__contains__(c):
                for cat in categories:
                    if dic[c].__contains__(cat) is False:
                        dic[c].append(cat)
            else:
                dic[c] = [categories[0]]
                if len(categories) > 1:
                    for i in range(1, len(categories)):
                        dic[c].append(categories[i])

        row += 1

    os.chdir(parent)

    return dic


def add_ap_courses(dic):
    dic['APENGLANG'] = ['LA']
    dic['APENGLIT'] = ['LA']
    dic['APFRENLANG'] = ['FL']
    dic['APFRENLIT'] = ['LA']
    dic['APGERMAN'] = ['FL']
    dic['APITALIAN'] = ['FL']
    dic['APMACRO'] = ['SBA']
    dic['APMICRO'] = ['SBA']
    dic['APPSYCH'] = ['SBA']
    dic['APSPANLANG'] = ['FL']
    dic['APSPANLIT'] = ['LA']

    return dic


""" Methods to be called from main program """


def get_focus_area_list():
    """
    Returns a list of focus area courses in the format [BEE4800, BME3010, ...] from the BE Advised website

    The courses are obtained by looking at the text between any bullet point and any dash
    For courses that are cross listed (ie 4440/6440) the two courses are listed separately
    """

    parent = os.getcwd()
    os.chdir(parent + "/support_files/website_data")

    fa_list = []
    f = open("focus_area_raw_code.txt", "r")
    for l in f:
        if "•" in l:
            course = re.search("•(.*)–", l)
            course = course.group(1)
            course = course.replace("\xa0", " ")
            course = course.replace("/", " ")
            course = course.split()
            if len(course) > 2:
                course1 = course[0]+course[1]
                course2 = course[0]+course[2]
                fa_list.append(course1)
                fa_list.append(course2)
            else:
                course1 = course[0] + course[1]
                fa_list.append(course1)
    f.close()

    os.chdir(parent)

    research_etc = upload_courses_from_file("research_ta_etc.xlsx")
    for c in research_etc:
        fa_list.append(c)

    return fa_list


def get_full_libarts_dict():
    """
    This creates a dictionary of every liberal arts course (key) and a list of every category that course can fulfill
    (value)
    """

    """
    Start off by reading the liberal arts courses from the website (actually, from the website data that's been saved 
    in the folder /website_data)
    """

    parent = os.getcwd()
    os.chdir(parent + "/support_files/website_data")

    libarts_dict = {}

    ca_list = get_category_list(ca_file)
    for c in ca_list:
        libarts_dict[c] = ["CA"]

    ha_list = get_category_list(ha_file)
    for c in ha_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("HA")
        else:
            libarts_dict[c] = ["HA"]

    kcm_list = get_category_list(kcm_file)
    for c in kcm_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("KCM")
        else:
            libarts_dict[c] = ["KCM"]

    la_list = get_category_list(la_file)
    for c in la_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("LA")
        else:
            libarts_dict[c] = ["LA"]

    sba_list = get_category_list(sba_file)
    for c in sba_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("SBA")
        else:
            libarts_dict[c] = ["SBA"]

    ce_list = get_category_list(ce_file)
    for c in ce_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("CE")
        else:
            libarts_dict[c] = ["CE"]

    os.chdir(parent)

    """
    Now, add in the "other yes" courses and ap courses
    """
    libarts_dict = add_other_yes(libarts_dict)
    libarts_dict = add_ap_courses(libarts_dict)

    return libarts_dict


def main():
    """
    Just used for debugging some of the methods used here
    This file is never called by itself, the methods are just called independently within or elsewhere in the program
    """

    refresh_focus_areas()
    refresh_libarts_all()


if __name__ == "__main__":
    main()
