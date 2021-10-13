"""
input = [[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]]
output = 123698745
"""

inp = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
x, y, z = inp[::]
level = max(len(y), len(z))
print(x, y, z)
res = [i for i in x]
for i in range(-1, level-1):
    res.append((y[i], z[i]))

print(res)
    

        
