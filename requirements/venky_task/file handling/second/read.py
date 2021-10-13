
with open("venky.txt",'r')as f:
  
  print(f.tell())
  f.seek(8)
  print(f.tell())
  print(f.read())
  print(f.tell())
