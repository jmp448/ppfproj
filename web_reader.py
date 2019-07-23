import requests
import re
import os


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

    r = requests.get(fa_url)
    fa_code = open(fa_file, "w")
    fa_code.write(r.text)
    fa_code.close()


def refresh_libarts_all():
    refresh_libarts_ca()
    refresh_libarts_ce()
    refresh_libarts_ha()
    refresh_libarts_kcm()
    refresh_libarts_sba()
    refresh_libarts_la()


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


def get_libarts_list(filename):
    """
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


""" Methods to be called from main program """


def get_focus_area_list():
    """The courses are obtained by looking at the text between any bullet point and any dash
    For courses that are cross listed (ie 4440/6440) the two courses are listed separately
    """

    parent = os.getcwd()
    os.chdir(parent + "/website_data")

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
                # TODO verify treatment of cross-listing
                course1 = course[0]+course[1]
                course2 = course[0]+course[2]
                fa_list.append(course1)
                fa_list.append(course2)
            else:
                course1 = course[0] + course[1]
                fa_list.append(course1)
    f.close()
    # TODO fix CHEME66XX - will never be used due to X's

    os.chdir(parent)

    return fa_list


def get_full_libarts_dict():
    """This creates a dictionary of every liberal arts course (key) and a list of every category that course can fulfill
    (value)
    """
    parent = os.getcwd()
    os.chdir(parent + "/website_data")

    libarts_dict = {}

    ca_list = get_libarts_list(ca_file)
    for c in ca_list:
        libarts_dict[c] = ["CA"]

    ha_list = get_libarts_list(ha_file)
    for c in ha_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("HA")
        else:
            libarts_dict[c] = ["HA"]

    kcm_list = get_libarts_list(kcm_file)
    for c in kcm_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("KCM")
        else:
            libarts_dict[c] = ["KCM"]

    la_list = get_libarts_list(la_file)
    for c in la_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("LA")
        else:
            libarts_dict[c] = ["LA"]

    sba_list = get_libarts_list(sba_file)
    for c in sba_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("SBA")
        else:
            libarts_dict[c] = ["SBA"]

    ce_list = get_libarts_list(ce_file)
    for c in ce_list:
        if libarts_dict.keys().__contains__(c):
            libarts_dict[c].append("CE")
        else:
            libarts_dict[c] = ["CE"]

    os.chdir(parent)

    return libarts_dict


def main():
    fa_list = get_focus_area_list()
    libart_dict = get_full_libarts_dict()

    # print(len(fa_list))
    print(libart_dict["HIST1620"])


if __name__ == "__main__":
    main()
