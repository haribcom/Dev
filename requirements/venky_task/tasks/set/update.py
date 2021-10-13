a={1,2}
a.add(3)
print(a)

print()
a.update([4,5,"venky",(56,10)],{7,8,9})
print(a)

b={1,2,3}
print(b)


c={4,5,6}
print()
c.update(b)
print(c)
b.update(c)
print(b)
