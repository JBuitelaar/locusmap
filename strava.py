import browser_cookie3
from datetime import datetime
from pathlib import Path
import requests
import json
from collections import namedtuple

# parameters:
provider_id = 99901  # needs to be unique across Locus maps
filename = Path().home() / "Downloads" / "strava.xml"
suffix = ' jb'  # add to the name (if anything)

# for every map: (Name to display, url field, color)
provider_fields = [
    ("Biking", "ride", "bluered"),
    ("Running", "run", "bluered")
]

cookie_names = [
    "CloudFront-Key-Pair-Id",
    "CloudFront-Policy",
    "CloudFront-Signature"
]


def get_cookies_from_browser():
    """read the relevant cookies from the browser after you've logged in to Strava via FireFox"""
    cj = browser_cookie3.firefox(domain_name='strava.com')
    cj.clear_expired_cookies()  # not sure this does anything

    cookies = [c for c in cj if c.name in cookie_names]
    return cookies


def get_cookies_from_api():
    # see: https://github.com/nnngrach/strava_auto_auth
    auth_url = 'https://api.apify.com/v2/acts/nnngrach~strava-auth/run-sync?token=ATnnxbF6sE7zEZDmMbZTTppKo'
    cookie_url = 'https://api.apify.com/v2/acts/nnngrach~strava-auth/runs/last/dataset/items?token=ATnnxbF6sE7zEZDmMbZTTppKo'

    with open('strava_login.json') as f:
        data = json.load(f)
    assert data['password'] != "*", "update password in strava_login.json"
    res = requests.post(auth_url, json=data)
    assert 201 == res.status_code
    cookies_list = requests.get(cookie_url).json()

    # make it look like a cookie object:
    cookie = namedtuple('cookie', ('name', 'value', 'expires'))
    cookies = [cookie(c['name'], c['value'], c['expires']) for c in cookies_list if c['name'] in cookie_names]
    return cookies


def get_cookie(cookies):
    assert len(cookies) == 3
    expiry_dt = datetime.fromtimestamp(min(c.expires for c in cookies))
    assert expiry_dt > datetime.now(), f"Cookies expired on {expiry_dt}"
    print("Cookies will expire on ", expiry_dt)
    assert len(cookies) == len(cookie_names), "not all cookie elements found"
    cookie_txt = "; ".join(f"{c.name}={c.value}" for c in cookies)
    return cookie_txt


content_format = """<?xml version="1.0" encoding="UTF-8"?>
<providers>

{}

</providers>"""

if __name__ == "__main__":
    cookies = get_cookies_from_api()
    # alternatively, you could use this, but you'd first need to login to strava using Firefox
    # cookies = get_cookies_from_browser()
    cookie_txt = get_cookie(cookies)

    template = open('strava_template.xml').read()

    providers = [
        template.format(id=provider_id + idx, name=name, type=activity, cookie=cookie_txt, suffix=suffix, color=color)
        for idx, (name, activity, color) in enumerate(provider_fields)
    ]

    content = content_format.format("\n\n".join(providers))

    with open(filename, 'w+') as f:
        f.write(content)
