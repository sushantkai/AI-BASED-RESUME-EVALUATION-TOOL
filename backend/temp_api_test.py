import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

url_login = 'http://127.0.0.1:8001/api/auth/login'
payload_login = json.dumps({'username': 'admin', 'password': 'admin123'}).encode('utf-8')
req_login = Request(url_login, data=payload_login, headers={'Content-Type': 'application/json'})
try:
    with urlopen(req_login, timeout=10) as r:
        login = json.loads(r.read().decode('utf-8'))
        print('login ok')
except Exception as e:
    print('login error', e)
    raise

url_create = 'http://127.0.0.1:8001/api/candidates'
payload_create = json.dumps({'name': 'Test User', 'email': 'testuser1234@example.com', 'phone': '9876543210'}).encode('utf-8')
req_create = Request(url_create, data=payload_create, headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {login['access_token']}"})
try:
    with urlopen(req_create, timeout=10) as r:
        print('create status', r.status)
        print(r.read().decode('utf-8'))
except HTTPError as e:
    print('HTTPError', e.code)
    print(e.read().decode('utf-8'))
except URLError as e:
    print('URLError', e.reason)
except Exception as e:
    print('error', e)
