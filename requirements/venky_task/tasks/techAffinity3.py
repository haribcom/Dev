l={"abc","bca","money","cba","def","yemon"}
t=tuple(l)
b=set()

for i in t:
  for j in range(len(t)):
    if sorted(i) == sorted(t[j]):
      print(t[j])
      
    
