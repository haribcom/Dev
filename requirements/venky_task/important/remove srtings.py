def venky(s):
  a="a,e,i,o,u"
  for i in s:
    if i not in a:
      #print("".join(i),end="")
      print(i,end="")
    

n=input("enter a string: ")
venky(n)
