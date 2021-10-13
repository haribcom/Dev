"""
input = 1112333122234
output = {1:2, 2:2, 3:2, 'leftout':1}
"""

inp = '1112333122234'
d = {}.fromkeys(inp, 0)
#print(d)
for i in inp:
    if i in d.keys():
        d[i] +=1
print(d)
for k, v in d.items():
    if v % 2 == 0:
        print("{} : {}".format(k, v//2))
    else:
        print("left out :", v)
