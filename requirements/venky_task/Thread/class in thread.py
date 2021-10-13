import threading
from  threading import *

class mythread(threading.Thread):
  def run(self):
    print("venky")
  def run(self):
    print("df")
t=mythread()
t.start()
