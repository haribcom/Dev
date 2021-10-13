import csv
with open("venky.csv","w") as f:
  a=csv.writer(f)
  a.writerow(["sno","name","course","addres","phone num"])
  while True:
    sno=int(input("enter sno: "))
    name=input("enter a name: ")
    course=input("enter course: ")
    address=input("enter a address: ")
    phone=int(input("enter a phone number: "))
    a.writerow([sno,name,course,address,phone])
    option=input("do you  want insert one more reocrd[y\n]: ")
    if option.islower()=="no":
      break
print("file succesfully")
  
    
