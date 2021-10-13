import numpy as np
n=int(input("enter no. of elements that u want :"))
a=[]
for i in range(n):
    ele=input("enter elements :")
    a.append(ele)
avrg= np.average(a)
print (a)
print ("Average is :",avrg)
