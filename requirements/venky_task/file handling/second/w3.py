s="""What is Python language
Python is a widely used high-level, general-purpose, interpreted, 
languages such as C++ or Java. 
Python supports multiple programming paradigms, including object-oriented,"""

def file(s):
  with open("venkat.pdf","w")as f:
    f.write(s)
    print("data stored into a file venkat.txt")
file(s)


def file_read(fname):
  with open(fname,'r')as f2:
    r=f2.read()
    n=0
    for i in r.splitlines():
      print(i)
      n=n+1
      if n==2:
        break
file_read("venkat.pdf")



import collections
a="venk venkat venkyy venkat venkat"
print(collections.Counter(a.split()))






















