from requests import get

print(get('http://127.0.0.1:5000/api/posts').json())

print(get('http://127.0.0.1:5000/api/posts/1').json())
