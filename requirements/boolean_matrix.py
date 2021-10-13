'''
Given a boolean matrix mat [M][N] of size M*N, modify it such that if a matrix cell mat[i][j] is 1(True), then make all the cells of ith row and jth column as 1.
inp = [0, 1, 0] [0, 0, 0] [0, 0, 0]
out = [1, 1, 1] [0, 1, 0] [0, 1, 0]
'''

inp = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]



#s = "102202103044012"
###out = "0000012"
##l = [[0, 1, 0],
##         [0, 0, 0],
##         [0, 0, 0]]
##for i in range(len(l)):
##    for j in range(len(l)):
##        if l[i][j] == 1:
##            k = 0
##            while k<len(l):
##                l[i][k] =l[j][] =  1
##                k+=1
##
##print(l)


# Python3 Code For A Boolean Matrix Question 
R = 3
C = 4

def modifyMatrix(mat): 
	row = [0] * R 
	col = [0] * C 
	
	# Initialize all values of row[] as 0 
	for i in range(0, R): 
		row[i] = 0
	print(row)	
	# Initialize all values of col[] as 0 
	for i in range(0, C) : 
		col[i] = 0
	print(col)

	# Store the rows and columns to be marked 
	# as 1 in row[] and col[] arrays respectively 
	for i in range(0, R) : 
		
		for j in range(0, C) : 
			if (mat[i][j] == 1) : 
				row[i] = 1
				col[j] = 1
			
	# Modify the input matrix mat[] using the 
	# above constructed row[] and col[] arrays 
	for i in range(0, R) : 
		
		for j in range(0, C): 
			if ( row[i] == 1 or col[j] == 1 ) : 
				mat[i][j] = 1
				
# A utility function to print a 2D matrix 
def printMatrix(mat) : 
	for i in range(0, R): 
		
		for j in range(0, C) : 
			print(mat[i][j], end = " ") 
		print() 
		
# Driver Code 
mat = [ [0, 1, 0], 
             [0, 0, 0], 
             [0, 0, 0] ] 

print("Input Matrix n") 
printMatrix(mat) 

modifyMatrix(mat) 

print("Matrix after modification n") 
printMatrix(mat) 

# This code is contributed by Nikita Tiwari. 
