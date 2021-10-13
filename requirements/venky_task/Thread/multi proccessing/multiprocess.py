import time
import multiprocessing

def venky(number):
  for i in number:
    print("square's :",i*i)
def venn(number):
  for j in number:
    print("double's:",j*2)
if __name__=="__main__":
  n=[1,2,5,6,8,6]
  t1=multiprocessing.Process(target=venky,args=(n,))
  t2=multiprocessing.Process(target=venn,args=(n,))
  t1.start()
  t2.start()
