import threading
import time
from threading import*
def ven():
  print(current_thread().name,"....started")
  time.sleep(3)
  print(current_thread().name,"....ended")

print("the no'f active thread is :",active_count())
t1=Thread(target=ven,name="Thread-1")
t2=Thread(target=ven,name="Thread-2")
t3=Thread(target=ven,name="Thread-3")
t1.start()
t2.start()
t3.start()
l=enumerate()
for i in l:
  print("thread name: ",i.name)
  print("The identifiactions is :",i.ident)
  print()
time.sleep(4)
l=enumerate()
for i in l:
  print("thread name: ",i.name)
  print("The identifiactions is :",i.ident)
  print()
