'''
s = ' me and mom asked uncle to meet dad'
find out 1st and last polindrom words and swap  the word and print the string

inp = ' me and mom asked uncle to meet dad'
out = ' me and mom asked uncle to meet mom'
'''

s = 'me and mom asked uncle to meet dad'.casefold()
s1 = s.split()
res = []
#print(s1)
for i in s1:
    if i == i[::-1]:
        res.append(i)
        print(s1.index(i))
print(res)

    
    

