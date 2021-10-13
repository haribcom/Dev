import re
mail = input("enter email : ")
m = re.match(r"[\w\-\_\.]{1,8}@[a-zA-Z]{1,6}\.[a-zA-Z]{1,3}", mail)
if m:
    print(True)
else:
    print(False)




##def check_valid(email):
##    try:
##        username, url = email.split("@")
##        website, extension = url.split(".")
##    except ValueError :
##        return False
##
##        if not username.replace("-", "").replace("_", "").isalnum():
##            return False
##        if not website.isalnum():
##            return False
##        if not len(extension) == 2 or len(extension) == 3:
##            return False
##    return True
##    
##
##n = int(input('enter range :'))
##emails = [input('enter emails :') for email in range(n)]
##
##valid = list(filter(check_valid, emails))
##print(sorted(valid))















        
