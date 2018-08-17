# Create column hopping function 
def colhop(curr,steps=1):
	currCol = curr[0]
	currRow = curr[1:]

	letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	loc = 0
	while letters[loc] != currCol:
		loc += 1
		if loc == len(letters):
			print('Error with column hopping')

	final_pos = loc+steps
	if final_pos < 0 or final_pos >= len(letters):
		print('Error with column hopping')
	else:
		return(letters[final_pos]+str(currRow))

#Create row hopping function
def rowhop(curr,steps=1):
	currCol = curr[0]
	currRow = curr[1:]

	dest = int(currRow)+steps

	if dest <= 0:
		print('Error with row hopping')
	else:
		return(currCol+str(dest))