d={1:4,5:6,2:8,4:7,3:5,6:9,7:2}

print(d)
print()

b=sorted(d.items())
print(b)

print()
from operator import itemgetter
sort_d=sorted(d.items(),key=itemgetter(1))
print(sort_d)

print()
d1={"name":"venky","age":24}
f=itemgetter("age")
print(f(d1))
f2=itemgetter("name")
print(f2(d1))

