def venky(s,t):
  c=s[:2]+t[2:]
  d=t[:2]+s[2:]
  printn(d+" "+c)

n=input("enter a string:")
m=input("enter a string:")
venky(n,m)
