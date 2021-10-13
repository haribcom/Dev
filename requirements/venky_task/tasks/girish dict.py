a=[{"ab":"venkat"},{"bc":"haha"},{"cba":"venky"},{"ada":"giri"},{"aba":"python"}]
b=[]
c=[]
for i in a:
  for j in i.keys():
    b.append(j)
b.sort()
for k in b:
  for h in a:
    for l in h.items():
      if k==l[0]:
        c.append(h)
print(c)




    


