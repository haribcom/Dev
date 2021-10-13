with open("venky.txt",'a')as f:
  f.write("How are you")
  
  with open("venky.txt",'r')as f2:
    print(f2.read())
    print(f)
    print(f2.mode)
    print(f.mode)
    print(f.closed)
    print(f.name)
