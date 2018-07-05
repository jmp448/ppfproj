function M = mapInit()
    % Create course mapping
    M = containers.Map('KeyType','char','ValueType','any');

    % List of Required Courses
    calcI = CourseReq;
    calcI.req = "calcI";
    calcI.options = ["MATH 1910",calcI.options];
    M('MATH1910')=calcI;

    calcII = CourseReq;
    calcII.req = "calcII";
    calcII.options = ["MATH 1920",calcII.options];
    M('MATH1920')=calcII;

    diffEq = CourseReq;
    diffEq.req = "diffEq";
    diffEq.options = ["MATH 2930",diffEq.options];
    M('MATH2930') = diffEq;

    linAlg = CourseReq;
    linAlg.req = "linAlg";
    linAlg.options = ["MATH 2940",linAlg.options];
    M('MATH2940') = linAlg;

    mech = CourseReq;
    mech.req = "mech";
    mech.options = ["PHYS 1112",mech.options];
    M('PHYS1112') = mech;

    electro = CourseReq;
    electro.req = "electro";
    electro.options = ["PHYS 2213", electro.options];
    M('PHYS2213') = electro;

    genChem = CourseReq;
    genChem.req = "genChem";
    genChem.options = ["CHEM 2070", "CHEM 2090", genChem.options];
    M('CHEM2070') = genChem;
    M('CHEM2090') = genChem;

    orgo = CourseReq;
    orgo.req = "orgo";
    orgo.options = ["CHEM 1570", "CHEM 3530", "CHEM 3570", orgo.options];
    M('CHEM1570') = orgo;
    M('CHEM3530') = orgo;
    M('CHEM3570') = orgo;

    introBio1 = CourseReq;

    introBio2 = CourseReq;

    introBioLab = CourseReq;
    introBioLab.req = "introBioLab";
    introBioLab.options = ["BIOG 1500", introBioLab.options];
    M('BIOG1500') = introBioLab;

    % TO DO: BioMG 3310 and 3320 are two courses for the one req
    biochem = CourseReq;
    biochem.req = "biochem";
    biochem.options = ["BIOMG 3300", "BIOMG 3330", "BIOMG 3310", "BIOMG3320", "BIOMG 3350", biochem.options];
    M('BIOMG3300') = biochem;
    M('BIOMG3330') = biochem;
    M('BIOMG3310') = biochem;
    M('BIOMG3320') = biochem;
    M('BIOMG3350') = biochem;
    
    cs = CourseReq;
    cs.req = "cs";
    cs.options = ["CS 1112", "BEE1510", cs.options];
    M('CS1112') = cs;
    M('BEE1510') = cs; %TODO verify

    statics = CourseReq;
    statics.req = "statics";
    statics.options = ["ENGRD 2020", statics.options];
    M('ENGRD2020') = statics;

    stats = CourseReq;
    stats.req = "stats";
    stats.options = ["CEE 3040", "ENGRD 2700", stats.options];
    M('CEE3040') = stats;
    M('ENGRD2700') = stats;

    introEng = CourseReq;

    thermo = CourseReq;
    thermo.req = "thermo";
    thermo.options = ["BEE 2220", "ENGRD 2210", "CHEME 3130", "MSE 3030",thermo.options];
    M('BEE2220') = thermo;
    M('ENGRD2210') = thermo;
    M('CHEME3130') = thermo;
    M('MSE3030') = thermo;
    
    engDist = CourseReq;
    engDist.req = "engDist";
    engDist.options = ["BEE 2600", "BEE 2510", engDist.options];
    M('BEE2600') = engDist;
    M('BEE2510') = engDist;

    fluids = CourseReq;
    fluids.req = "fluids";
    fluids.options = ["BEE 3310", fluids.options];
    M('BEE3310') = fluids;

    biomat = CourseReq;
    biomat.req = "biomat";
    biomat.options = ["BEE 3400", biomat.options];
    M('BEE3400') = biomat;

    hm = CourseReq;
    hm.req = "hm";
    hm.options = ["BEE 3500", hm.options];
    M('BEE3500') = hm;

    molec = CourseReq;
    molec.req = "molec";
    molec.options = ["BEE 3600", molec.options];
    M('BEE3600') = molec;

    inst = CourseReq;
    inst.req = "inst";
    inst.options = ["BEE 4500", inst.options];
    M('BEE4500') = inst;

end