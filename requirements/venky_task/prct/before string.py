def venky(str):
    if len(str)>=2 and str[:2]=="is":
        return str
    else:
        return "is"+str
print(venky('venky'))
print(venky("isvenky"))
