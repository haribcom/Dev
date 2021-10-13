import re
with open("D:\\vv\\venky1236.txt","r")as f1:
  with open("output.txt","w")as f2:

    for i in f1:
      a=re.findall("[6-9]\d{9}",i)
      for j in a:
        print(j)
        f2.write(j+"\n")
