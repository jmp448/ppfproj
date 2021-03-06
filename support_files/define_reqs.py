from support_files.Category import Category
from support_files.ReqTypes import BasicCourseReq,  MultiCourseReq, ApprovedElectives
from support_files.web_reader import get_focus_area_list, get_full_libarts_dict
from support_files.helper_tools import upload_courses_from_file

'''
Create objects used to store PPF data
'''


def create_category_list():

    calcI = BasicCourseReq('Calc I', threshold="C-", options=['MATH1910', 'APCALC'], position=12)
    calcII = BasicCourseReq('Calc II', threshold="C-", options=['MATH1920'], position=13)
    diffEq = BasicCourseReq('Diff Eq', threshold="C-", options=['MATH2930'], position=14)
    linAlg = BasicCourseReq('Lin Alg', threshold="C-", options=['MATH2940'], position=15)
    math = Category('Math', [calcI, calcII, diffEq, linAlg], 'M15', 16)

    mech = BasicCourseReq('Mechanics', options=['PHYS1112', 'APMECH'], position=19)
    electromag = BasicCourseReq('Electromagnetism', options=['PHYS2213', 'PHYS2208', 'APELECTRO'], position=20)
    phys = Category('Physics', [mech, electromag], 'M20', 8)

    gen_chem = BasicCourseReq('Gen Chem', options=['CHEM2070', 'CHEM2090', 'CHEM2150', 'APCHEM'], position=23)
    orgo = BasicCourseReq('Orgo', options=['CHEM1570', 'CHEM3530', 'CHEM3570', 'CHEM3590', 'CHEM3600', 'CHEM3890', 'CHEM3900'], position=24)
    chem = Category('Chemistry', [gen_chem, orgo], 'M24', 7)

    intro_bio = MultiCourseReq('Intro Bio', creds_needed=6, options=['BIOMG1350', 'BIOG1440', 'BIOG1445', 'BIOEE1610',
                                                                     'BIOSM1610', 'APBIO4', 'APBIO5-1', 'APBIO5-2'],
                               positions=[27, 28])
    bio_lab = BasicCourseReq('Intro Bio Lab', options=['BIOG1500', 'BIOSM1500', 'APBIOLAB'], position=29)
    biochem = MultiCourseReq('Biochemistry', creds_needed=4, options=['BIOMG3300', 'BIOMG3330', 'BIOMG3350', 'BIOMG3310',
                                                                      'BIOMG3320'], positions=[30, 31])
    adv_bio_courses = upload_courses_from_file("./support_files/advanced_bio.xlsx")
    adv_bio = MultiCourseReq('Advanced Biology', creds_needed=3, options=adv_bio_courses, positions=[32, 33])
    bio = Category('Biological Sciences', [intro_bio, bio_lab, biochem, adv_bio], 'M32', 15)

    fws = MultiCourseReq('FWS', creds_needed=6, options=None, positions=[35, 36])
    fws = Category('First-Year Writing Seminar', [fws], 'M36', 6)

    libarts_dict = get_full_libarts_dict()
    libarts_courses = list(libarts_dict.keys())
    libarts = MultiCourseReq('Liberal Arts', options=libarts_courses, creds_needed=18,
                             positions=[49, 50, 51, 52, 53, 54, 55], libart=True)
    libarts = Category('Liberal Studies', [libarts], 'M57', 18)

    cs = BasicCourseReq('Computer Science', options=['BEE1510', 'CS1110', 'CS1112', 'APCS'], position=65)
    cs = Category('Computer Science', [cs], 'M65', 4)

    statics = BasicCourseReq('Statics', options=['ENGRD2020'], position=70)
    stats = BasicCourseReq('Statistics', options=['CEE3040', 'ENGRD2700'], position=71)
    engri = upload_courses_from_file("./support_files/engri_courses.xlsx")
    intro_eng = BasicCourseReq('Intro Engineering', options=engri, position=73)
    thermo = BasicCourseReq('Thermodynamics', options=['BEE2220', 'ENGRD2210', 'CHEME3130', 'MSE3030'], position=74)
    eng_dist = BasicCourseReq('Engineering Distribution', options=['BEE2600', 'BEE2510', 'ENGRD2600', 'ENGRD2510'], position=76)
    fluids = BasicCourseReq('Fluid Mechanics', options=['BEE3310'], position=77)
    biomat = BasicCourseReq('Biomaterials', options=['BEE3400'], position=78)
    heat_mass = BasicCourseReq('Heat and Mass', options=['BEE3500'], position=79)
    cell_bioeng = BasicCourseReq('Molecular and Cellular Bioengineering', options=['BEE3600'], position=80)
    bioinst = BasicCourseReq('Bioinstrumentation', options=['BEE4500'], position=81)
    fa_list = get_focus_area_list()
    focus_areas = MultiCourseReq('Focus Areas', options=fa_list, creds_needed=15, positions=[84, 85, 86, 87, 88])
    eng_core = Category('Engineering Requirements', [statics, stats, intro_eng, thermo, eng_dist, fluids, biomat,
                                                     heat_mass, cell_bioeng, bioinst, focus_areas], 'M90', 48)

    approved_electives = ApprovedElectives()
    approved = Category('Approved Electives', [approved_electives], 'M95', min_creds=6)

    category_list = [math, phys, chem, bio, fws, libarts, cs, eng_core, approved]

    return category_list
