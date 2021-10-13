import re

def valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)

    return bool(m) and all(map(lambda x: 0<=int(x) <= 255, m.groups()))

print(valid_ip(input('enter valid ip : ')))


