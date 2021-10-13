from threading import *
def display():
  for i in range(10):
    print("Child Thread\t")
    
t=Thread(target=display) # or Thread(target=display).start()
t.start()           
for i in range(10):
  print("Main Thread")

