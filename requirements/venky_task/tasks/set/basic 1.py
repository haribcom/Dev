s={1,2,3,5,6,7}
t={4,5,6,9,8}
print(sum(s))
print(min(s))
print(max(s))
s.update(t)
print(s)
t.update(s)
print(t)

print()
s.add(200)
print(t)
print(s)

s.remove(5)
print(s)
s.discard(200)
print(s)
s.pop()
print(s)
t.clear()
print(t)

