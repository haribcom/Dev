import re
count=0
'''with open("input.txt","r") as f:
  with open("venky.txt","w") as f2:
    for i in f:
      m=re.findall(r"[6-9]\d{9}",i)
      for j in m:
        f2.write(j+'\n')
      print(f.read())'''







with open("input.txt","r") as f:
  
  with open("output.txt","w") as f1:
    for i in f:
      r=re.findall(r"[6-9]\d{9}",i)
      
      for j in r:
        count=count+1
        f1.write(j+'\n')
print('totally ',count,'numberes are saved')
print("all numbers are stored in ouput.txt file")
        



'''f=open("input.txt","w")
f.write("""venky venkafh \n 96665963028
          dad 9502811182
          venky 7989431107 venky venka  78965896589
          jdfdhfkjf""")
f.close()'''
