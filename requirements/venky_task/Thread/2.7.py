from threading import *
def display():
  for i in range(10):
    print("Child Thread\t")
    
Thread(target=display).start()
for i in range(10):
  print("Main Thread")
