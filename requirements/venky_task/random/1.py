import random
items=["venky","venn","vennyy","venkat"]
c=random.choices(items, k=3)
a=random.choice(items)
print("choice ",a)
print("choices",c)
b=random.shuffle(items)
print("shuffle ",b)

t=[10,2,3,5,12,45,999,22,33,55,66,55,88,55,44,55]
p=[10,5,8,6,5]
next=["next time better luck"]
i=random.choices(t, next)
print(i)
