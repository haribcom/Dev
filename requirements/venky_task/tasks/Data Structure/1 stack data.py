"A B C D"
class data():
  def __init__(self):
    self.items=[]
    
  def push(self,i):
    self.items.append(i)
    
  def get(self):
    return self.items
    
  def pop(self):
    self.items.pop()

  def empty(self):
    return self.items==[]
  def peek(self):
    if not self.empty():
      return self.items[-1]
      
      
A=data()
print(A.empty())
A.push("a")
A.push("b")
A.push("c")
print(A.get())
print(A.empty())
print(A.peek())


