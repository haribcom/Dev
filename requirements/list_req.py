## X=’ab12c3d’ find list = [123]

x='ab12c3d'
l1 = []
for i in list(x):
    try:
        l1.append(int(i))
    except:
        pass
print(l1)
