import matplotlib.pyplot as plt
x=[1,2,3,4,5,6,7,8,9]
y=[5,6,8,2,3,7,5,6,9]
plt.scatter(x,y,label="skitscat",color="R",s=25,marker="o")
plt.xlabel("x")
plt.ylabel("y")
plt.title("my graph")
plt.legend()
plt.show()
