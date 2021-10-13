import matplotlib.pyplot as plt
import numpy as np

a=["java","python","oracle","html"]
b=[50,90,40,60]
jobs=[20,60,40,20]
yp=np.arange(len(a))
plt.barh(yp-0.5,b,label="Reiew")
plt.ylabel("ratio")
plt.barh(yp-0.2,jobs,label="jobs")
plt.xticks(yp,b)
plt.legend()
plt.show()
 
