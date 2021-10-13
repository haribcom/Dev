# Python 3.x code to demonstrate star pattern
 
# Function to demonstrate printing pattern triangle

from __future__ import print_function # for end = " " in print syntax.

def triangle(n):
     i = 0
     while i<=n:
          print( " " * (2*n-i), "* " * (i+1))
          i+=1
          j = 0
     while j<=n:
          print(" " * (2*n-i), "* " * (i))
          i -=1
          j +=1


     
##     k = 2*n - 2
##     for i in range(0, n):
##         for j in range(0, k):
##             print(end=" ")
##         k = k - 1
##         for j in range(0, i+1):
##             print("* ", end=" ")
##         print()


         

n = 5
triangle(n)










