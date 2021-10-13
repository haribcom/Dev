'''
#1) sorting order standing
l = [2, 7, 5, 9, 6, 11, 8, 10]
res = [l[0]]
#print(res)
for i in l:
    if res[-1] < i:
        res.append(i)
print(res)


#2) duplicate elimination
a = [1, 2, 2, 3, 1, 4, 5, 4]
b = []
for i in a:
    if a.count(i) ==1:
        b.append(i)
print(b)
'''

#3) Given an array of integers, write a function that returns True 
#    if there is a triplet (a, b, c) that satisfies a2+b2 = c2 

l = [3, 1, 4, 5, 6]
sol = []
for i in range(len(l)):
    for j in range(i+1, len(l)):
        for k in range(j+1, len(l)):
            if (l[i]**2) + (l[j]**2) == (l[k]**2):
                sol.append((l[i], l[j], l[k]))
            else:
                pass
if sol:
    print(True)
    print("this is pythagram triplet ", sol)
else:
    print(False)
    print("this is not a pythagram triplet ")


'''
4) squers in dict
a = [1, 2, 3, 4]
d = {}
for i in a:
    d[i] = i**2
print(d)

res = {i:i**2 for i in a}
print(res)

'''
