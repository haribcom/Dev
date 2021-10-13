## Function which returns subset or r length from n 
##from itertools import combinations
##import time
##
##def rSubset(arr, r): 
##
##	# return list of all subsets of length r 
##	# to deal with duplicate subsets use 
##	# set(list(combinations(arr, r))) 
##	return list(combinations(arr, r)) 
##
## Driver Function 
##if __name__ == "__main__": 
##	arr = [1, 2, 3, 4, 5] 
##	r = 2
##	st = time.clock()
##	print(rSubset(arr, r))
##	et = time.clock()
##	do = et-st
##	print(do)






l = [1, 2, 3, 4, 5]
res = []

for i in range(len(l)):
    for j in range(i+1, len(l)):
        if l[i] == l[j]:
            continue
        else:
            res.append(tuple((l[i], l[j])))

print(res )















