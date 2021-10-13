import collections
my_list = ["a","b",'a',"c","e"]
ctr = collections.Counter(my_list)
print("Frequency of the elements in the List : ",ctr)

a=[1,2,5,4,5,6,5,4,5,211,1,4]
a1=collections.Counter(a)
print(a1)


b=collections.Counter("venkyvenkat")
print(b)

ctr1 =collections.Counter({'birds': 200, 'lizards': 340, 'hamsters': 120})
print(ctr1)
