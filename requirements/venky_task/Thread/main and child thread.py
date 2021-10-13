#import threading
from threading import *
def venky():
  for i in range(1):
    print("The child thread is \t: ",current_thread().getName())
    def venn():
      print("\t the second functions is: ",current_thread().getName())
    Thread(target=venn).start()
t=Thread(target=venky)
t.start()




for j in range(1):  
  print("the main thread is : ",current_thread().getName())
