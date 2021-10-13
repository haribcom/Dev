import matplotlib.pyplot as plt
import numpy as np
a=[1,2,3,4,5,6,7,8,9]
b=[2,3,5,6,9,4,5,4,5]
plt.histh(a,label="age")
plt.histh(b,label="papulation")
plt.title("Histogram graph")
plt.legend()
plt.show()
