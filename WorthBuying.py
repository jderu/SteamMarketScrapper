import ast
from datetime import datetime
from statistics import mean

minimum_sold_skins = 5
minimum_profit_procent= 0.225
min_price= 7

class Item:

    def __init__(self, name, price_history=[]):
        self.name = name
        self.price_history = price_history
    
    def __str__(self):
        return self.name + ": " + str(self.price_history)

def get_items(in_file_name,out_file_name):
    existing_items = []
    with open(in_file_name, 'r', encoding="utf-16") as file:
        i = 0
        for line in file:
            if i == 0:
                i = 1
            else:
                divider = line.find(": [")
                old_item = Item(line[:divider], ast.literal_eval(line[divider + 2:-1]))
                existing_items.append(old_item)
        file.close()
    
    for i in existing_items:
        sold_skins = 0
        skin_prices = []
        for j in reversed(i.price_history):
            if (datetime.now() - datetime.strptime(j[0], '%b %d %Y %H: +0')).days > 60:
                break
            sold_skins += int(j[2])
            for _ in range(0, int(j[2])):
                skin_prices.append(float(j[1]))
        if sold_skins >= minimum_sold_skins:
            skin_prices=sorted(skin_prices)
            #first or last x%
            interval_start=int(len(skin_prices)*0.10)+1 #2
            interval_end=int(len(skin_prices)*0.3)+1 #4
            #if the price for the top (x% * the profit) is greater than the bottom x% and the price is greater than min_price
            bottomx= mean(skin_prices[interval_start:interval_end])
            topx = mean(skin_prices[-interval_end:-interval_start])
            
            if  topx * (1-0.15-minimum_profit_procent) > bottomx and topx > min_price:
                print(i.name,", bottom%:",int(bottomx*100)/100,", top%:",int(topx*100)/100)

get_items("218620.txt","218620.out")
print("\nCS:GO\n")
get_items("730.txt","730.out")

x = input("finished")
