a=["1",2,3]
b=set()
for i in a:
  b.add(i)
print(b)


print()
c={1,2,3,4,5,6}
c.add(7)
print(c)
c.pop()
print(c)
c.discard(5)
print(c)
print(help(set))
print()

z={7,9}
x={1,2,3,4,5,6}
y={4,5,6,7,8,9}
print(x|y)
print(y.union(x))
print(x&y)
print(y&x)
print(x.intersection(y))
print(x.difference(y))
print(y.difference(x))
print(x^y)
print(y^x)
print(y.symmetric_difference(x))


print()
print(x.isdisjoint(z))












