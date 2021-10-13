a={1 :"ball", 2 :"apple"}
print(a)
print()

b={1:"venky","a":1236,True:10.23,10+10j:(1,2,3),"tuple":(1,2,3),"list":[1,2,3,4],"set":{7,8,9}}

print(b)
for k,v in b.items():
  print(v,type(v))
  print(k,type(v))
