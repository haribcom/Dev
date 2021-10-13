def make_pretty(func):
  def inner():
    print("i got decorator")
    func()
    print("i got second line ")
    func()
    print("i got  third line")
    
  return inner
@make_pretty
def ordinary():
  print("i am ordinary")
ordinary()


