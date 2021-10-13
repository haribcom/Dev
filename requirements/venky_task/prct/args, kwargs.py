def venky(name,msg):
  print("Hello...",name,msg)
venky(msg="venky",name="Good morning...")
venky("venky",msg="Good morning...")
venky("venky","Good morning...")


print()
def foo(name,*args,**kwargs):
  print(name)
  if args:
    print("args are ", args)
  if kwargs:
    print(kwargs)
    
foo("venky")
foo("venkat","venn",10,20)
print()
foo("venkyy",10,20,30,venk=1236)

