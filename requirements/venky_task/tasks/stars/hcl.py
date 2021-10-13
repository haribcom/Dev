

def pattern(n):
  for i in range(4):
    for j in range(0,4-i-1):
      print(end=" ")
    for j in range(0,i+1):
      print(n,end=" ")
      n=n+1
    print()
pattern(1)





"""output:

          1
         2 3 
        4 5 6
       7 8 9 10 
"""
