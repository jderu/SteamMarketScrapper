import json
import ast
from selenium import webdriver
from time import sleep


class Item:

    def __init__(self, name, price_history=[]):
        self.name = name
        self.price_history = price_history
    
    def __str__(self):
        return self.name + ": " + str(self.price_history)


def get_items_name(file_name):
    items = []
    with open(file_name, 'r', encoding="utf-16") as file:
        for line in file:
            item_name = line.split("quantity:")[0][:-1]
            items.append(item_name)
    return items


def scrape_item(item, appid):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    try_count = 0
    while 1:
        print(item_number)
        site = "https://steamcommunity.com/market/listings/" + appid + "/" + item.name.replace("/", "-")
        driver.get(site)
        content = driver.page_source
        try:
            index1 = content.find("var line1=") + len("var line1=")
            if(index1 == len("var line1=") - 1):
                raise Exception()
            index2 = content.find("]];", index1) + len("]]")
            item.price_history = json.loads(content[index1:index2])
            driver.close()
            return item
        except:
            try_count += 1
            if(try_count == 6):
                return item
            sleep(30)


def save(out_file_name, items):
    with open(out_file_name, 'w', encoding="utf-16") as file:
        file.write(str(item_number))
        file.write("\n")
        for item in items:
            file.write(str(item))
            file.write("\n")
        file.close()


#in_file_name = "218620_3_2000.out"
in_file_name = "730_3_2000.out"

appid = in_file_name.split("_")[0]
out_file_name = appid + ".txt"

existing_items = []
item_number = 0
with open(out_file_name, 'r', encoding="utf-16") as file:
    i = 0
    for line in file:
        if i == 0:
            item_number = int(line)
            i = 1
        else:
            divider = line.find(": [")
            old_item = Item(line[:divider], ast.literal_eval(line[divider + 2:-1]))
            existing_items.append(old_item)
    file.close()

new_items = get_items_name(in_file_name)

while item_number < len(new_items):
    new_item = scrape_item(Item(new_items[item_number]), appid)
    ok = 1
    for i in range(0, len(existing_items)):
        if existing_items[i].name == new_item.name:
            if existing_items[i].price_history != new_item.price_history:
                print(existing_items[i].price_history[-2:])
                print(new_item.price_history[-2:])
                print(new_item.name, "updated")
            existing_items[i] = new_item
            ok = 0
    if ok == 1:
        existing_items.append(new_item)
        existing_items = [x for x in sorted(existing_items, key=lambda i:i.name)]
    save(out_file_name, existing_items)
    item_number = (item_number + 1) % len(new_items)
    sleep(3.5)
        
