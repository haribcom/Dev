class Remotecontrol():
    def __init__(self):
        self.channels=["matv","HBO","TEJATV","kalainger"]
        self.index=-1
    def __iter__(self):
        return self
    def __next__(self):
        self.index=self.index+1
        if self.index==len(self.channels):
            raise StopIteration
        return self.channels[self.index]

r=Remotecontrol()
itr=iter(r)
while True:
    try:
        print(next(itr))
        print(next(itr))
        print(next(itr))
        print(next(itr))
        print(next(itr))
    except(StopIteration):
        break
        

    
        
