
#input={"abc","bca","acb","money","yemon","def"}
#ouput={"abc","bca","acb"},{"def"},{"money","yemon"}
'''

s = 'heart'
s1 = 'earth'

##if sorted(s) == sorted(s1):
##    print(True)
##else:
##    Print(False)


def sort(s):
    for i in s:

s='rams'
s1='mar'
print(sorted(s))
print(s)
if sorted(s)==sorted(s1):
    print('trueee')
'''
ques={"abc","bca","acb","money","yemon","def"}
result=[]
for i in ques:
    #print(sorted(i))
    for j in ques:
        
        if sorted(i)==sorted(j):
            result.append((i,j))
print(result)
for i in result:
    if i[0]==i[1]:
        result.remove(i)
print(result)
