##l = [[10, 15, 30], [12, 15, 20], [17, 20, 32]]
##l1 = []
##for i in l:
##    for j in i:
##        l1.append(j)
##res = sorted(l1)
##print(res)


def merge(l):
    merge_list = []
    heap = [(1st[0], i, 0) for i, 1st in enumerate(l) if 1st]
    heapq.heapify(heap)
    while heap:
        val, list_ind, ele_ind = heapq.heappop(heap)
        merge_list.append(val)
        if ele_ind+1 < len(l[list_ind]):
            next_tuple = (l[list_ind][ele_ind+1], list_ind, ele_ind+1)
            heapq.heappush(heap, next_tuple)
            return merge_list

l = [[10, 15, 30], [12, 15, 20], [17, 20, 32]]
merge(l)
