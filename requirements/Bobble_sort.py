# a=[54, 26, 93, 17, 77, 31, 44, 55, 20]
# for i in range(0, len(a)):
#     for j in range(0, len(a)-i-1):
#         if(a[j]>a[j+1]):
#             a[j], a[j+1] = a[j+1], a[j]
# print (a)



def bubbleSort(L):
    for n in range(len(L)-1, -1, -1):
        for i in range(n):
            if L[i]>L[i+1]:
                L[i], L[i+1] = L[i+1], L[i]
L = [54,26,93,17,77,31,44,55,20]
bubbleSort(L)
print(L)

