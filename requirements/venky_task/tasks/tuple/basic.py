a=((11,),10.2,"",10+9j,{("f",):5},{'a':["venkay","venn"]},{5,10+5j,"venkat"},(1,2,5))

print(type(a),a)

for i in a:
  print(type(i))

print()

b=tuple(((11,),10.2,"",10+9j,{("f",):5},{'a':"venkay"},{5,10+5j,"venkat"},(1,2,5)))
print(type(b),[type(i) for i in a])

print(help(list))
