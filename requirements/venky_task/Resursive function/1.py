"""def myfun():
  print("Welcome")
  myfun()
myfun() """


i=0
def myfunc():
  print("venky")
  global i
  i=i+1
  while i<=5:
    myfunc()
myfunc()
