book={}

book["venky"]={"name":"venkatesh",
               "address":"tpt",
               "cource":"python",
               "phone":"9666596308"}

book["girish"]={"name":"giri",
               "address":"nlr",
               "cource":"python",
               "phone":"9799866523"}

import json
j=json.dumps(book)
print(type(j))
print(type(book))
