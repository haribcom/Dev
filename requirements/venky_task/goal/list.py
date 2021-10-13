import collections
a=[4,5,6,8,6,9,4,4,4,4,4,5,6]
x=collections.Counter(a)
print(collections.Counter(a))
print(x)


b=set()
c=set()
for  i in a:
  if i not in b:
    b.add(i)
  else:
    c.add(i)
print(b)
print(c)
print(list(b-c))


