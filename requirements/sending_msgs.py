import requests
import json
res = requests.post('https://textbelt.com/text', {
  'phone': '+918500769820',
  'message': 'Hello Honey',
  'key': 'textbelt',
})
result = res.json()
print(result)

