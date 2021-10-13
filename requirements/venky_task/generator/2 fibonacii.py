def fibi():
  a,b=0,1
  while True:
    yield a
    a,b=b,a+b
i=fibi()

for i in fibi():
  if i<100:
    print(i)
  
