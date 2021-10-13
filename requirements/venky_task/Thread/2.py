from threading import *
class x(Thread):
  def run(self):
    for i in range(10):
        print("child thread")
t=x()
t.start()
for i in range(10):
  print("main htread")
