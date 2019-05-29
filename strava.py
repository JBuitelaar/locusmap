import browser_cookie3
from datetime import datetime
from pathlib import Path

# parameters:
provider_id = 99901  # needs to be unique across Locus maps
filename = Path().home() / "Downloads" / "strava.xml"
suffix = ' jb'  # add to the name (if anything)

# for every map: (Name to display, url field, color)
provider_fields = [
    ( "Biking", "ride", "bluered" ),
    ( "Running", "run", "bluered" )
]


def get_cookie():
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
    # print(f'Cookie#{cookie_txt}')
    return cookie_txt


content_format = """<?xml version="1.0" encoding="UTF-8"?>
<providers>

{}

</providers>"""

if __name__ == "__main__":
    cookie_txt = get_cookie()
    template = open(str('strava_template.xml')).read()

    providers = [
        template.format(id=provider_id + idx, name=name, type=activity, cookie=cookie_txt, suffix=suffix, color=color)
        for idx, (name, activity, color) in enumerate(provider_fields)
    ]

    content = content_format.format("\n\n".join(providers))

    with open(filename, 'w+') as f:
        f.write(content)
