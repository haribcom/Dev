def venky(s):
  n=s.find("not")
  m=s.find("poor")
  for i in s.split():
    if i=="not":
      c=s.replace(i,"poor")
      print(s[n:]+str(c))


n=input("enter a string :")
venky(n)
