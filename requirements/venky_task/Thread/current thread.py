import threading

print("the executing thread is ",threading.current_thread().getName())

from threading import *
print(current_thread().getName())

#To change a thread Name
print(current_thread().ident)
print(current_thread().name)
current_thread().setName("venky")
print(current_thread().name)

