stdin = str(input('enter your string : ')).casefold()
d = {}.fromkeys(stdin,0)

for i in stdin:
    if i in d.keys():
        d[i] += 1
        
stdout = ' '

for k, v in d.items():
    stdout += str(v) + k
    
print(stdout)


