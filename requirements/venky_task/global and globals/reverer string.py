s=input("enter a string:")
try:
  if int(s):
    rev=int(s[::-1])
    print(rev,type(rev))
    
    """l=len(s)-1
    for i in range(len(s)):
      p=l-i
      print(s[p],type(s[p]),end="",)    """
except:
  print(s[::-1])
