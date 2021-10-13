import csv
with open("venky.csv","a",newline='') as f:
  w=csv.writer(f)
  w.writerow(["sno","name","course","address","phone_num"])
  while True:
    sno=int(input("enter sno: "))
    name=input("enter a name: ")
    course=input("enter course: ")
    address=input("enter a address: ")
    phone_num=int(input("enter a phone number: "))
    w.writerow([sno,name,course,address,phone_num])
    option=input("do you  want insert one more reocrd[yes\no]: ")
    if option.lower()== "no":
      break
print("file succesfully")
  
    
