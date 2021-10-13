def maxConsecutive1(inp):
    print(max(map(len, inp.split('0'))))
inp = '11000111101010111'
maxConsecutive1(inp) 




inp = '11000111101010111'
s = inp.split('0')
count = 0
for i in s:
    if len(i) > count:
        count = len(i)
print(count)
        
