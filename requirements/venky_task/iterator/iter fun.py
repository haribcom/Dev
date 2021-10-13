class infiniter():
    """infinite iterator to return all old number"""
    def __init__(self,n):
        self.n=n
    def __iter__(self):
        self.num=1
        return self
    def __next__(self):
        num=self.n
        num=self.n+self.num
        return num
        
i=infiniter(10)
it=iter(i)
print(next(i))
print(next(i))

"""while True:
    try:
        print(next(it))
    except():
        break""" 
