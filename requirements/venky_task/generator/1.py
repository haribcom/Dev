def gen():
  yield "venky"
  yield "venkat"
for i in gen():
  print(i)

print()
i=gen()
print(next(i))
