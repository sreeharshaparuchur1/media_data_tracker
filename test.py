import requests

BASE = "http://127.0.0.1:5000/"

data = [{'name': 'House of Ballons', 'views': 10000, 'likes':10000},
        {'name': 'Or Nah', 'views': 1000000, 'likes':690000},
        {'name': 'I love it', 'views': 100000, 'likes':42000}]

for index, info in enumerate(data):
    response = requests.put(BASE + "video/" + str(index), info)
    print(response.json()) #Not printing a response object

input()
response = requests.delete(BASE + "video/0")
print(response) #Delete doesn't have any json serialized object attached to it
input()
response = requests.get(BASE + "video/2")
print(response.json()) #Not printing a response object
