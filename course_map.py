import class_structs as cs

def create():
	
	cm = {}

	calcI = cs.CourseReq(req_name='Calc I')
	cm['MATH1910']=calcI

	calcII = cs.CourseReq(req_name='Calc II')
	cm['MATH1920']=calcII

	diffeq = cs.CourseReq(req_name='Differential Equations')
	cm['MATH2930']=diffeq

	linalg = cs.CourseReq(req_name='Linear Algebra')
	cm['MATH2940']=linalg

	mech = cs.CourseReq(req_name='Mechanics')
	cm['PHYS1112']=mech
	
	electro = cs.CourseReq(req_name='Electromagnetism')
	cm['PHYS2213']=electro

	genchem = cs.CourseReq(req_name='Gen Chem')
	cm['CHEM2070']=genchem
	cm['CHEM2090']=genchem

	orgo = cs.CourseReq(req_name='Orgo')
	cm['CHEM1570']=orgo
	cm['CHEM3530']=orgo
	cm['CHEM3570']=orgo

	biolab = cs.CourseReq(req_name='Intro Bio Lab')
	cm['BIOG1500']=biolab

	#TODO: necessitate combination of biomg 3310 and 3320
	biochem = cs.CourseReq(req_name='Biochemistry')
	cm['BIOMG3300']=biochem
	cm['BIOMG3330']=biochem
	cm['BIOMG3310']=biochem
	cm['BIOMG3320']=biochem
	cm['BIOMG3350']=biochem

	#TODO: probably remove BEE 1510
	compsci = cs.CourseReq(req_name='Computer Science')
	cm['CS1112']=compsci
	cm['BEE1510']=compsci

	statics = cs.CourseReq(req_name='Statics')
	cm['ENGRD2020']=statics

	stats = cs.CourseReq(req_name='Statistics')
	cm['CEE3040']=stats
	cm['ENGRD2700']=stats

	thermo = cs.CourseReq(req_name='Thermodynamics')
	cm['BEE2220']=thermo
	cm['ENGRD2210']=thermo
	cm['CHEME3130']=thermo
	cm['MSE3030']=thermo

	engdist = cs.CourseReq(req_name='Engineering Distribution')
	cm['BEE2600']=engdist
	cm['BEE2510']=engdist

	fluids = cs.CourseReq(req_name='Fluid Mechanics')
	cm['BEE3310']=fluids

	biomat = cs.CourseReq(req_name='Biomaterials')
	cm['BEE3400']=biomat

	heatnmass = cs.CourseReq(req_name='Heat and Mass Transfer')
	cm['BEE3500']=heatnmass

	molec = cs.CourseReq(req_name='Cell and Molecular Bioengineering')
	cm['BEE3600']=molec

	inst = cs.CourseReq(req_name='Bioinstrumentation')
	cm['BEE4500']=inst

	#TODO remove
	introbee=cs.CourseReq(req_name='Introduction to BEE')
	cm['BEE1200']=introbee

	return cm