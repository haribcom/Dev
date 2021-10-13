a={1,2,3,4}
b={3,4,5,6,85,56}
print(a.issubset(b))
print(a<=b)
print(b.issubset(a))

print(a.issuperset(b))
print(a>=b)

print()
print(a.union(b));print(b|a)
print()
print(a.intersection(b));print(b&a)
print()
print(a.difference(b));print(b-a)
print()
print(a.symmetric_difference(b));print(b^a)

print()

s={12,"venky",(1,2,3)}
print(s)
