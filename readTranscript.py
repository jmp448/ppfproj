from openpyxl import load_workbook
import numpy as np
import hop
import class_structs as cs
import course_map
import os

def read_transcript():

	wb = load_workbook(filename='transcript.xlsx',data_only=True)

	transcript = wb.active

	# Figure out what columns contain what info
	pos = 'A1'
	curr = transcript[pos].value
	cols={}

	while curr != None:
		if curr == 'Academic Term Sdescr':
			cols['semester'] = pos[0]
		elif curr == 'Effdt Primary Name':
			cols['name'] = pos[0]
		elif curr == 'Netid':
			cols['netid'] = pos[0]
		elif curr == 'Employee Id':
			cols['emplid'] = pos[0]
		elif curr == 'Advisor':
			cols['advisor'] = pos[0]
		elif curr == 'Exp Grad Term Sdescr':
			cols['grad'] = pos[0]
		elif curr == 'Class Descr':
			cols['desc'] = pos[0]
		elif curr == 'Subject':
			cols['subj'] = pos[0]
		elif curr == 'Catalog Nbr':
			cols['num'] = pos[0]
		elif curr == 'Official Grade':
			cols['grade'] = pos[0]
		elif curr == 'Unt Taken':
			cols['creds'] = pos[0]

		pos = hop.colhop(pos)
		curr = transcript[pos].value

	# Create the list of course requirements and corresponding options
	cm = course_map.create()

	# Create class objects
	class Class(object):
		def __init__(self,file=transcript,row=None,cols=None):

			dept_loc = cols['subj']+row
			num_loc = cols['num']+row
			self.course_num = file[dept_loc].value + str(file[num_loc].value)

			creds_loc = cols['creds']+row
			self.creds = file[creds_loc].value

			grade_loc = cols['grade']+row
			self.grade = file[grade_loc].value

	# Read class objects off of transcript and update course map accordingly
	curr_row = 2
	name_loc = cols['name'] + str(curr_row)
	curr_stud = transcript[name_loc].value

	# 
	while transcript[name_loc].value == curr_stud:
		curr_class = Class(row=str(curr_row),cols=cols)
		if curr_class.course_num in cm:
			cm[curr_class.course_num].fillby(curr_class)
		curr_row += 1
		name_loc = cols['name'] + str(curr_row)

	return cm

# Produce summary document for the student
os.chdir(os.getcwd()+'/Students')

summary = open(curr_stud + ".txt","w+")
for key in cm:
	if cm[key].taken==True:
		summary.write("%s was satisfied by %s \n" % (cm[key].req_name, cm[key].class_name))
