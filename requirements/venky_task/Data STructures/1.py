a=["venky","python","django","venkat"]

def create_dataset():
  import random
  r=50
  f=open("venky.txt","w")
  for _ in range(r):
    current=random.choice(a)
    f.write(current+"\n")
  f.close()
create_dataset()

    
  
