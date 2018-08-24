"""
@file: 
@time: 
@author: 
@contact: 
@desc: 

"""
from requests.cookies import cookiejar_from_dict

__author__ = 'hanhw'


import requests
import json

# r = requests.request('GET', 'https://api.github.com/events', stream=True)
# r.raise_for_status()
# print(r.status_code)
# print(r.encoding)
# print(r.content)
# print(r.text)
# print(r.json())
# print(r.raw.read())
# print(str(r.raw.read(decode_content=True), encoding='utf-8'))

# try:
#     content = str(r.raw.read(), encoding='utf-8', errors='replace')
# except (LookupError, TypeError):
#     # A LookupError is raised if the encoding was not found which could
#     # indicate a misspelling or similar mistake.
#     #
#     # A TypeError can be raised if encoding is None
#     #
#     # So we try blindly encoding.
#     content = str(r.raw.read(), errors='replace')
# print(content)
# print(r.text)
# with open('stream', 'wb', encoding='utf-8') as fd:
#     fd.write(r.raw.read())


# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('http://httpbin.org/cookies')
# print(r.text)
#
# s = requests.Session()
# # s.auth('user', 'pass')
# s.cookies = cookiejar_from_dict({'cd': '2323'})
# s.headers.update({'x-test': 'true'})
# r = s.get('http://httpbin.org/headers', headers={'x-test2': 'true'}, cookies={'abc': '123'})
# print(r.text)

r = requests.get('https://requestb.in')
print(r.status_code)
r.raise_for_status()
print(r.text)
