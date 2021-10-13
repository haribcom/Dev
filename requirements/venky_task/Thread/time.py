import time
import threading
def square(numbers):
  for i in numbers:
    time.sleep(1)
    print("the squares is :",i*i)
def double(self):
  for i in numbers:
    time.sleep(1)
    print(" the doubles is :",i+i,"\t")


numbers=[1,2,3,4,5,6]
start_time=time.time()
t1=threading.Thread(target=square,args=(numbers,))
t2=threading.Thread(target=double,args=(numbers,))
t1.start()
t2.start()
t1.join()
t2.join()
end_time=time.time()
print("total time taken: ",end_time-start_time)


"""start_time=time.time()
square(numbers)
double(numbers)
end_time=time.time()
print("total time taken: ",end_time-start_time)"""

