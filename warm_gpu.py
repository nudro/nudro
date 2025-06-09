import requests

from time import sleep

r = requests.get('http://10.136.89.254:5000/on')

print(r.status_code)
print(r.headers)

sleep(600)

r = requests.get('http://10.136.89.254:5000/off')

print(r.status_code)
print(r.headers)

