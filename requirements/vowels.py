''' Find the no.of alphabets b/w 1st and 2nd Vowels .
 if no.of vowels less then 2 in the string return -1
 inp : Hello    o/p : 2
'''

l = 'Hello'
v = ('a', 'e', 'i', 'o', 'u')
res = []
i=0
while i < len(l):
    if l[i] in v:
        res.append(i)
    i+=1
#print(res)
out = int(res[-1]-res[0]-1)

if  (out)>= 2:
    print(out)
else:
    print("-1")
    
