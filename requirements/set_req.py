"""
inp = {1, 2, 3}
out = {{}, {1}, {2}, {3}, {1, 2}, {1, 3}, {2,3}, {1, 2, 3}}
"""
from math import pow

inp = [1, 2, 3]
s = [{}, set(inp)]

for i in range(len(inp)):
    j=i
    while j<len(inp):
        if i == j:
            s.append({inp[i]})
        else:
            s.append({inp[i], inp[j]})
        j+=1

print(s)







# python3 program for power set


# def printPowerSet(inp,set_size):
#
#
#     pow_set_size = int(math.pow(2, set_size))
#
#
#     for counter in range(0, pow_set_size):
#         for j in range(0, set_size):
#
#             if((counter & (1 << j)) > 0):
#                 print(inp[j], end = "")
#         print("")
#
# inp = [1, 2, 3]
# printPowerSet(inp, 3)


