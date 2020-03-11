import json

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.proxy import Proxy, ProxyType

file_name = "Repository/data.txt"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("log-level=3")
chrome_options.add_argument("--headless")


def get_proxies():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")
        if result[-1] == "yes":
            PROXIES.append(result[0] + ":" + result[1])

    driver.close()
    return PROXIES


def proxy_driver(PROXIES):
    prox = Proxy()
    if PROXIES:
        pxy = PROXIES[-1]

    else:
        print("--- Proxies used up (%s)" % len(PROXIES))
        PROXIES = get_proxies()

    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = prox.ssl_proxy = pxy

    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
    return driver


ALL_PROXIES = get_proxies()
print(ALL_PROXIES)
driver = proxy_driver(ALL_PROXIES)
running = True

while running:
    try:
        print("--- Switched proxy to: %s" % ALL_PROXIES[-1])
        for i in range(0, 10):
            driver.get(
                "https://steamcommunity.com/market/search/render/?search_descriptions=0&norender=1&count=100&sort_column=quantity&sort_dir=asc&appid=440&start=0")
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            print("try:", i + 1)

        ALL_PROXIES.pop()
        driver = proxy_driver(ALL_PROXIES)
        sleep(1)

    except:
        print("Actual fucking exception")
        print("--- Switched proxy to: %s" % ALL_PROXIES[-1])
        ALL_PROXIES.pop()
        driver = proxy_driver(ALL_PROXIES)
        sleep(1)
