import matplotlib.pyplot as plt
x=[1,2,3]
y=[4,5,8]
x1=[7,8,9]
y2=[4,5,6]
plt.plot(x,y,label="First line")
plt.plot(x1,y2,label="second label")
plt.xlabel("Plot Number")
plt.ylabel("Important var")
plt.title(" Interesting  graph and check it")
plt.legend()

plt.show()

