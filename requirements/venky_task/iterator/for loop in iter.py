iterable=[1,23,32,4]
for element in iterable:
    
    iter_obj = iter(element)
while True:
    try:
        element = next(iter_obj)
    except StopIteration:
        break
iterable=[1,23,32,4]
for element in iterable:
    
    iter_obj = iter(element)
