%{
Josh Popp
Program Progress Form Updater
Cornell University BEE Department
Created: 14 Jun 2018
Last modified: 14 Jun 2018
%}

%{
Purpose: This program automatically creates and updates 
    program progress forms for biological engineering students
    based on the curriculum as of 2018
%}

%{ 
Input:

Output:
    Program progress forms for each student with the name 'smithj'
    (last name first initial) reflecting the course information 
    present in the excel file
    
%}

% Create course mapping
M = containers.Map('KeyType','char','ValueType','any');

% List of Required Courses
calcI = CourseReq;
calcI.options = ["MATH 1910",calcI.options];
M('MATH1910')=calcI;

calcII = CourseReq;
calcII.options = ["MATH 1920",calcII.options];
M('MATH1920')=calcII;

diffEq = CourseReq;
diffEq.options = ["MATH 2930",diffEq.options];
M('MATH2930') = diffEq;

linAlg = CourseReq;
linAlg.options = ["MATH 2940",linAlg.options];

mech = CourseReq;
mech.options = ["PHYS 1112",mech.options];

electro = CourseReq;
electro.options = ["PHYS 2213", electro.options];

genChem = CourseReq;
genChem.options = ["CHEM 2070", "CHEM 2090", genChem.options];

orgo = CourseReq;
orgo.options = ["CHEM 1570", "CHEM 3530", "CHEM 3570", orgo.options];

introBio1 = CourseReq;

introBio2 = CourseReq;

introBioLab = CourseReq;
introBioLab.options = ["BIOG 1500", introBioLab.options];

% TO DO: BioMG 3310 and 3320 are two courses for the one req
biochem = CourseReq;
biochem.options = ["BIOMG 3300", "BIOMG 3330", "BIOMG 3310", "BIOMG3320", "BIOMG 3350", biochem.options];

cs = CourseReq;
cs.options = ["CS 1112", cs.options];

statics = CourseReq;
statics.options = ["ENGRD 2020", statics.options];

stats = CourseReq;
stats.options = ["CEE 3040", "ENGRD 2700", stats.options];

introEng = CourseReq;

thermo = CourseReq;
thermo.options = ["BEE 2220", "ENGRD 2210", "CHEME 3130", "MSE 3030"];

engDist = CourseReq;
engDist.options = ["BEE 2600", "BEE 2510", engDist.options];

fluids = CourseReq;
fluids.options = ["BEE 3310", fluids.options];

biomat = CourseReq;
biomat.options = ["BEE 3400", biomat.options];

hm = CourseReq;
hm.options = ["BEE 3500", hm.options];

molec = CourseReq;
molec.options = ["BEE 3600", molec.options];

inst = CourseReq;
inst.options = ["BEE 4500", inst.options];

[~,name] = xlsread('transcript','B2');
