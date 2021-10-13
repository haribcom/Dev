import numpy as np
import sys
import time

l=range(1000)
print(sys.getsizeof(2)*len(l))

array=np.arange(1000)
print(array.size*array.itemsize)


l=["abcd", "ab", "bc", "abc"]
for x in l:
  if len(l)>3:
    i.insert(0, i)
    print(l) 
