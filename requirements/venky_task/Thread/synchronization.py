import threading
import time

class x(threading.Thread):
  def run(self):
    lc.acquire()
    myfun("django")
    lc.release()
class y(threading.Thread):
  def run(self):
    lc.acquire()
    myfun("flask")
    lc.release()
def myfun(msg):
  print("{ hello [",msg)
  time.sleep(5)
  print("] world }")
lc=threading.Lock()
x1=x()
y1=y()
x1.start()
y1.start()

