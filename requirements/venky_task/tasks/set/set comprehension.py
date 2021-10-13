x={p for p in range(10)}
print(x)


y={q*q for q in range(20) if q%2==0}
print(y)

print()
a=set(["mango","apple"])
b=set(["mango","orange"])
c=set(["mango"])

print(a>=b)
print(a<=b)
print(a>c)
print(c>b)
print(c<b)

