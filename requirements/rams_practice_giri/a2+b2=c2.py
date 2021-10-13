#3) Given an array of integers, write a function that returns True 
#    if there is a triplet (a, b, c) that satisfies a2+b2 = c2 

x=range(20,50)
#print(x)
l=[]
result=[]
for i in x:
    l.append(i)
#print(l)
for x in range(len(l)):
    #print(x)
    for y in range(x+1,len(l)):
        #print(y)
        for z in range(y+1,len(l)):
            if (l[x]**2)+(l[y]**2)==(l[z]**2):
                result.append((l[x],l[y],l[z]))
if result:
    print('yes',result)
                
