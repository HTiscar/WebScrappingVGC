from lxml.html import fromstring
import requests
import numpy as np
from itertools import cycle


def get_proxies(num=None):
    link = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all&ssl=all&anonymity=all&uptime=100"
    proxies = list(requests.get(link).text.split())
    np.random.shuffle(proxies)

    proxies = []
    if len(proxies) == 0:
        proxies = list(requests.get(link[:-3] + '99').text.split())
        np.random.shuffle(proxies)
    print('Found', len(proxies), 'proxies, testing them now')

    if num is None:
        num = len(proxies)
    tested = test_proxies(proxies, num)
    return tested


def test_proxies(proxies, num):
    url = 'https://httpbin.org/ip'
    proxy_pool = cycle (proxies)
    working_proxies = []
    for i in range(1, len(proxies)):
        if num == 0:
            break
        proxy = next (proxy_pool)
        print("Request #%d" % i)
        try:
            response = requests.get(
                url, proxies={"http": proxy, "https": proxy}, timeout=1)
            print(response.json())
            working_proxies.append(proxy)
            num -= 1
        except:
            print("Skipping. Connnection error")
            pass
    return working_proxies