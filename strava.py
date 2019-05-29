import browser_cookie3
from datetime import datetime

# parameters:
id = 99901  # needs to be unique across Locus maps
filename = "strava"
suffix='jb'

cj = browser_cookie3.firefox(domain_name='strava.com')
cj.clear_expired_cookies()  # not sure this does anything

cookie_names = [
    "CloudFront-Key-Pair-Id",
    "CloudFront-Policy",
    "CloudFront-Signature"
]

cookie_elements = []
max_expiry = 0
for cookie in cj:
    if cookie.name in cookie_names:
        cookie_elements.append(f"{cookie.name}={cookie.value};")
        max_expiry = max(max_expiry, cookie.expires)

expiry_dt = datetime.fromtimestamp(max_expiry)

assert len(cookie_elements) == len(cookie_names), "not all cookie elements found"
assert expiry_dt > datetime.now(), f"Cookies expired on {expiry_dt}"

cookie_txt = "".join(cookie_elements)
#print(f'Cookie#{cookie_txt}')

# todo: generalize template for other colours and sports. Can create multiple providers as they are all the same
template = open('strava_template.xml').read()
content = template.format(id1=id, id2=id + 1, cookie=cookie_txt, suffix=suffix)

with open(f'{filename}.xml', 'w+') as f:
    f.write(content)
