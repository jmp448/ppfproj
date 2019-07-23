from Category import Category
from ReqTypes import BasicCourseReq,  MultiCourseReq, FillinCourseReq
from web_reader import get_focus_area_list
from web_reader import get_full_libarts_dict
from helper_tools import upload_adv_bio

'''
Create objects used to store PPF data
'''


def create_category_list():

    calcI = BasicCourseReq('Calc I', threshold="C-", options=['MATH1910'], position=12)
    calcII = BasicCourseReq('Calc II', threshold="C-", options=['MATH1920'], position=13)
    diffEq = BasicCourseReq('Diff Eq', threshold="C-", options=['MATH2930'], position=14)
    linAlg = BasicCourseReq('Lin Alg', threshold="C-", options=['MATH2940'], position=15)
    math = Category('Math', [calcI, calcII, diffEq, linAlg], 'M15', 16)

    mech = BasicCourseReq('Mechanics', options=['PHYS1112'], position=19)
    electromag = BasicCourseReq('Electromagnetism', options=['PHYS2213'], position=20)
    phys = Category('Physics', [mech, electromag], 'M20', 8)

    gen_chem = BasicCourseReq('Gen Chem', options=['CHEM2070', 'CHEM2090'], position=23)
    orgo = BasicCourseReq('Orgo', options=['CHEM1570', 'CHEM3530', 'CHEM3570'], position=24)
    chem = Category('Chemistry', [gen_chem, orgo], 'M24', 7)

    intro_bio = MultiCourseReq('Intro Bio', creds_needed=6, options=['BIOMG1350', 'BIOG1440', 'BIOG1445', 'BIOEE1610', 'BIOSM1610'],
                               positions=[27, 28])
    bio_lab = BasicCourseReq('Intro Bio Lab', options=['BIOG1500', 'BIOSM1500'], position=29)
    biochem = MultiCourseReq('Biochemistry', creds_needed=4, options=['BIOMG3300', 'BIOMG3330', 'BIOMG3350', 'BIOMG3310',
                                                                      'BIOMG3320'], positions=[30, 31])
    adv_bio_courses = upload_adv_bio()
    bio = Category('Biological Sciences', [intro_bio, bio_lab, biochem], 'M32', 15)
    adv_bio = FillinCourseReq('Advanced Biology', options=adv_bio_courses, category=bio, positions=[32, 33])
    bio.reqs.append(adv_bio)

    fws = MultiCourseReq('FWS', creds_needed=6, options=None, positions=[35, 36])
    fws = Category('First-Year Writing Seminar', [fws], 'M36', 6)

    libarts_dict = get_full_libarts_dict()
    libarts_courses = libarts_dict.keys()
    libarts = MultiCourseReq('Liberal Arts', options=libarts_courses, creds_needed=18,
                             positions=[49, 50, 51, 52, 53, 54, 55], libart=True)
    libarts = Category('Liberal Studies', [libarts], 'M57', 18)

    cs = BasicCourseReq('Computer Science', options=['BEE1510', 'CS1112'], position=65)
    cs = Category('Computer Science', [cs], 'M65', 4)

    statics = BasicCourseReq('Statics', options=['ENGRD2020'], position=70)
    stats = BasicCourseReq('Statistics', options=['CEE3040', 'ENGRD2700'], position=71)
    intro_bee = BasicCourseReq('Intro Engineering', options=['BEE1200'], position=73)
    thermo = BasicCourseReq('Thermodynamics', options=['BEE2220', 'ENGRD2210', 'CHEME3130', 'MSE3030'], position=74)
    eng_dist = BasicCourseReq('Engineering Distribution', options=['BEE2600', 'BEE2510'], position=76)
    fluids = BasicCourseReq('Fluid Mechanics', options=['BEE3310'], position=77)
    biomat = BasicCourseReq('Biomaterials', options=['BEE3400'], position=78)
    heat_mass = BasicCourseReq('Heat and Mass', options=['BEE3500'], position=79)
    cell_bioeng = BasicCourseReq('Molecular and Cellular Bioengineering', options=['BEE3600'], position=80)
    bioinst = BasicCourseReq('Bioinstrumentation', options=['BEE4500'], position=81)
    fa_list = get_focus_area_list()
    focus_areas = MultiCourseReq('Focus Areas', options=fa_list, creds_needed=15, positions=[84, 85, 86, 87, 88])
    eng_core = Category('Engineering Requirements', [statics, stats, intro_bee, thermo, eng_dist, fluids, biomat,
                                                     heat_mass, cell_bioeng, bioinst, focus_areas], 'M90', 48)


    # TODO phys ed

    # TODO capstone

    # TODO lab

    category_list = [math, phys, chem, bio, fws, libarts, cs, eng_core]

    return category_list
