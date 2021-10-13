import copy
l1 = [1, [2, 3], 4, 5]

print(l1, "id is : ",id(l1))

l2 =copy.copy(l1) # shallow copy

print(l2, "id is : ",id(l2))

l2[1][0] = 0

print('l2 is : ', l2, 'l1 is : ', l1)

l3 = [1, [2, 3], 4, 5]

print(l3, "id is : ",id(l3))

l4 = copy.deepcopy(l3)  # deepcopy

print(l4, "id is : ",id(l4))

l4[1][0] = 0

print('l4 is : ', l4, 'l3 is : ', l3)
