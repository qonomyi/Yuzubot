import re

import requests

base = "https://act.hoyolab.com/app/zzz-game-record/"

js_in_html_pattern = r"pc_\w+\.js"
js_in_init_js_pattern = r'\{1:"?\w{8,8}"?(,?\w+:"?\w{8,8}"?)+\}'


def fetch_all_js():
    raw_html = requests.get(
        "https://act.hoyolab.com/app/zzz-game-record/index.html"
    ).text

    it = re.finditer(js_in_html_pattern, raw_html)
    js_ids = []
    for i in it:
        data = requests.get(base + i.group()).text
        with open("./scripts/cache/" + i.group(), "w", encoding="utf-8") as f:
            f.write(data)

        r = None
        print(i.group())

        try:
            r = re.finditer(js_in_init_js_pattern, data)
            id_match = [i.group() for i in r][-1]
            p = re.findall(r'(\w+):"?(\w+)"?', id_match)
            # print(r.group())

            js_ids = [v for _, v in p]
        except Exception as e:
            print(e)
            continue

    print(js_ids)

    for id in js_ids:
        print(id)
        name = f"pc_{id}.js"
        data = requests.get(base + name).text
        with open("./scripts/cache/" + name, "w", encoding="utf-8") as f:
            f.write(data)
