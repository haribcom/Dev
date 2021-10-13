import os
fname=input("enter a file name: ")
if os.path.isfile(fname):
  f=open(fname,'r')
  cwords=clines=cchar=0
  print(f.read())
  for i in f:
    clines+=1
    words=i.split()
    #print(i)
    lwords=len(words)
    cwords=cwords+len(words)
    cchar=cchar+len(i)
    #print("",lwords)
  print("The numbers of char : ",cchar)
  print("The number of words in :",cwords)
  print("The number of lines in :",clines)
  f.close()
else:
  print("file not exits here...please try again....")
