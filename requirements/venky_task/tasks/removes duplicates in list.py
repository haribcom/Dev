a=[4,5,6,8,6,9,5,6]

def remove(a):
  b=[]
  c=[]
  for i in a:
    if i not in b:
      b.append(i)
    else:
      c.append(i)
  return (list(set(b)-set(c)))
print(remove(a))


mylist = ["a", "b", "a", "c", "c"]
print(list(dict.fromkeys(mylist)))

d={1:"venky",2:"python"}
print(list(d.values()))
print(list(d.keys()))
print(list(d.items()))
print(list(dict.fromkeys(d)))

