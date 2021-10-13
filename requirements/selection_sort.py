def sort(l):
    for i in range(len(l)-1):
        s = i
        j=i
        while j<len(l):
            if l[j] < l[s]:
                s = j
            j+=1
        l[i], l[s] = l[s], l[i]
        


l = [3, 1, 4, 2, 6, 9, 5, 4, 7]
sort(l)
print(l)
