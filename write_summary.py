import os

def write_summary(cm):
	# Produce summary document for the student
	os.chdir(os.getcwd()+'/Students')

	# summary = open(curr_stud + ".txt","w+")
	summary = open("jmp448.txt","w+")
	for key in cm:
		if cm[key].taken==True:
			summary.write("%s was satisfied by %s \n" % (cm[key].req_name, cm[key].class_name))
