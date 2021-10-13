l = [{'firstname':'Gireesh', 'lastname':'Nasina'},{'firstname':'honey', 'lastname':'priya'} ]

for i in l:
    if i['firstname'].startswith('Gir'):
        print(list(j for j in i.values()))