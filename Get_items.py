import json
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


def get_items(appid, file_name):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    n = a = 0
    
    open(file_name, 'w')
    with open(file_name, 'w+', encoding="utf-16") as file:
        while 1:
            site = "https://steamcommunity.com/market/search/render/?search_descriptions=0&norender=1&count=100&sort_column=name&sort_dir=asc" + "&appid=" + str(appid) + "&start=" + str(n)
            driver.get(site)
            content = driver.page_source
            soup = BeautifulSoup(content, features="html.parser")
            try:
                f = soup.find('pre').text
                if f != "null":
                    data = json.loads(f)
                    if len(data["results"]) == 0:
                        break
                    for i in data["results"]:
                        a += 1
                        file.write(i["name"] + " quantity: ")
                        file.write(str(i["sell_listings"]) + " price: ")
                        file.write(i["sale_price_text"] + "\n")
                    n += 100
                    sleep(3.5)
                else:
                    sleep(35)
            except:
                sleep(1)


def sort_and_cut(in_file_name, out_file_name, min_price, max_price, min_quantity=1, max_quantity=10000, reverse=False):
    try:
        open(in_file_name, 'x', encoding="utf-16")
    except:
        pass
    try:
        open(out_file_name, 'x', encoding="utf-16")
    except:
        pass
    
    new_items = []
    with open(in_file_name, 'r', encoding="utf-16") as file:
        for line in file:
            tmp = line.split("quantity:")
            item = []
            item_name = tmp[0]
            item_quantity = int(tmp[1].split("price:")[0])
            item_price = float(tmp[1].split("price:")[1].replace(',', '').replace('$', ''))
            item.append(item_name)
            item.append(item_quantity)
            item.append(item_price)
            new_items.append(item)
            
    old_items = []
    with open(out_file_name, 'r', encoding="utf-16") as file:
        for line in file:
            tmp = line.split("quantity:")
            item = []
            item_name = tmp[0]
            item_quantity = int(tmp[1].split("price:")[0])
            item_price = float(tmp[1].split("price:")[1].replace(',', '').replace('$', ''))
            item.append(item_name)
            item.append(item_quantity)
            item.append(item_price)
            old_items.append(item)
    
    for item in new_items:
        old_items.append(item)
    old_items = [x for x in sorted(old_items, key=lambda i:i[0])]
    new_items = [old_items[0]]
    for i in range(1, len(old_items)):
        if old_items[i - 1][0] != old_items[i][0]:
            new_items.append(old_items[i])
    new_items = [x for x in sorted(new_items, key=lambda i:i[2], reverse=reverse) if x[1] >= min_quantity and x[1] <= max_quantity and x[2] >= min_price and x[2] <= max_price]
            
    with open(out_file_name, 'w', encoding="utf-16") as file:
        print("Found", len(new_items), "items.")
        for item in new_items:
            out_string = item[0] + "quantity: " + str(item[1]) + " price: $" + str(item[2]) + "\n"
            file.write(out_string)
        
#########################################################################
# 730-CS:GO
# 218620-PD2
# 440-TF2


gameid = "218620"
min_price = 3
max_price = 2000
file_name = str(gameid) + "_" + str(min_price) + "_" + str(max_price)

for i in range(0, 5):
    print("Starting lap:", i + 1)
    get_items(gameid, file_name + ".in")
    sort_and_cut(file_name + ".in", file_name + ".out", min_price, max_price,3)
    
print("finished")
