import matplotlib.pyplot as plt

a=[0,1,2,3,4,5,6,7]
b=[10,30,20,40,60,50,70,80]

plt.plot(a,color="yellow",label="this is a no'of weeks",linewidth="9")
plt.plot(b,label="rate for the day",color="orange",ls="dotted",lw=8,marker="+",mec="Black")

plt.plot(a,color="blue",label="this is a no'of weeks",linewidth="1")
plt.title("my matplotlib  for AI")
plt.xlabel("x-axix")
plt.ylabel("Y-axix")
plt.legend()
plt.show()
