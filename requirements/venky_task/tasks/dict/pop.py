a={1:1,2:4,3:6,4:16,5:25}
print(a.pop(1))
print(a)
print()

print(a.popitem())
print(a)

del a[4]
print(a)

print(list(sorted(a.keys())))
