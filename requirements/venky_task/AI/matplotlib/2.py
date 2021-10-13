import matplotlib.pyplot as plt


a=[0,1,2,3,4,5,6,7]
b=[10,12,13,14,15,12,16,12]
c=[20,28,26,24,26,27,21,28]
d=[41,47,49,45,43,49,45,46]
plt.title("My Graph")
plt.plot(a,label="first")
plt.plot(a,c,label="second")
plt.plot(a,d,label="third",lw=5)
plt.legend(loc="best",shadow=True)

plt.grid()
plt.show()

