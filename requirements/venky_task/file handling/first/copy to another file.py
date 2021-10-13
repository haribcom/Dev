
# import re
# with open("abc.txt","r") as f:
#   for i in f:
#     m=re.findall("STUPIDSGEMS",i)
#     for i in m:
#       print(i)



f1=open("abc.txt")
f2=open("abcd.txt","a")
f2.write(f1.read())
f2.close()
f1.close()
print("the date copied venkat to venky:")
