class Divider:
    def __init__(self, n, num):
        self.ele = num
        self.n = n
    def __iter__(self):
        self.num = num
        return self
    def __next__(self):
        self.res = 0
        if self.num <= self.n:
            self.res += self.num
            self.num += self.ele
        else:
            raise StopIteration
        return self.res

num = int(input("enter number : "))
n = int(input("enter Range : "))
obj = Divider(n, num)

iter_obj = iter(obj)

while True:
    try:
        print(next(iter_obj))
    except StopIteration:
        break
