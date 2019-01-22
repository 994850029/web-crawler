import re

import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}

login_url = 'https://github.com/login'

login_response = requests.get(login_url, headers=headers)
login_token = re.search('name="authenticity_token" value="(.*?)"', login_response.text).group(1)
print(login_token)
login_cookie = login_response.cookies.get_dict()
print(login_cookie)

session_url = 'https://github.com/session'

session_response = requests.post(
    session_url,
    headers=headers,
    cookies=login_cookie,
    data={
        "commit": "Sign in",
        "utf8": "✓",
        "authenticity_token": login_token,
        "login": "yangyuanhu",
        "password": "123654asd"
    }
)

print(session_response.text)
