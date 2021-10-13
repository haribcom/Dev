import sys
print(sys.argv)

try:
  a=sys.argv[1]
  x=int(a)
  b=sys.argv[3]
  y=int(b)
  print(x+y)
except(ValueError):
  print("arguments pass only integer.....OK")
except(IndexError):
  print("pleas ente only two values....OK")
        
