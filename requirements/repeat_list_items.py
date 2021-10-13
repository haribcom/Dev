##list1 = ['giri','honey','giri','honey',2,3,'idiot','hari']
##mydict = {i:list1.count(i) for i in list1}
##print (mydict)



##from collections import Counter
##list1 = ['giri','honey','giri','honey',2,3,'idiot','hari']
##re_items = dict(Counter(list1))
##print (re_items)






L = ['giri','honey','giri','honey',2,3,'idiot','hari']
dup_dict = {}
for i in set(L):
    dup_dict[i] = L.count(i)
print (dup_dict)
