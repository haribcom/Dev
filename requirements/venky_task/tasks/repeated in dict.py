def rep(l):
  a=dict()
  for i in l:
    if i in a:
      a[i]+=1
    else:
      a[i]=1
  print(a)
  for j in a.items():
    if j[1]==1:
      print(j)
b=rep("venkyvenkat")

