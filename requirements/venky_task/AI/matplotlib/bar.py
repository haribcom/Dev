import matplotlib.pyplot as plt
import numpy as np

a=["java","python","oracle","html"]
b=[50,90,40,60]
jobs=[20,60,40,20]
yp=np.arange(len(a))
plt.bar(yp-0.5,b,label="Review",width=0.4)
plt.ylabel("ratio")
plt.bar(yp-0.5,jobs,label="jobs",width=0.3)
plt.xticks(yp,jobs)
plt.savefig("bar_graph.png",bbox_inches="tight")
plt.legend()
plt.show()
 
