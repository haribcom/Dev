with open("venky.txt","r") as f:
  wc=0
  ln=0
  cc=0
  s=""
  for i in f:
    ln=ln+1
    words=i.split()
    words=len(words)
    wc=wc+words
    
  print(ln)
  print(wc)
  
  #print(f1)
  
