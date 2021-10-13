
def foo(n):
  def mul(x):
    return x*n
  return mul
a=foo(5)
b=foo(5)
print(a(b(2)))


print(1,2,3,4,sep="*")
print()
