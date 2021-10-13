from pympler import summary

def fun1():
    x = (10, 'hi')
    return x

obj = fun1()
sum1 = summary.summarize(obj)
