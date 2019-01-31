import requests
from bs4 import BeautifulSoup
from requests import codes
from urllib.parse import urlencode
import pandas as pd

rankL = []
nameL = []
starL = []
amountL = []
quoteL = []

def get_page(offset):
    params = {
        "start": offset,
        "filter":""
    }
    base_url = "https://movie.douban.com/top250/?"
    url = base_url + urlencode(params)
    try:
        pageSource = requests.get(url)
        if codes.ok == pageSource.status_code:
            return pageSource.text
    except requests.ConnectionError:
        return None

def get_info(source):
    soup = BeautifulSoup(source, "html.parser")
    items = soup.find("ol", class_= "grid_view").find_all("li")
    for item in items:
        rank = item.find(class_="pic").text
        rankL.append(rank)
        name = item.find(class_="title").text
        nameL.append(name)
        star = item.find(class_="star").find_all("span")[1].text
        starL.append(star)
        amount = item.find(class_="star").find_all("span")[3].text
        amountL.append(amount)
        quote = item.find(class_="quote")
        if quote == None:
           quote = ""
        else:
            quote = quote.text
        quoteL.append(quote)
    return rankL, nameL, starL, amountL, quoteL

def save_info(info):
    rank = info[0]
    name = info[1]
    star = info[2]
    amount = info[3]
    quote = info[4]
    top250 = {"rank": rank, "name": name, "star": star, "amount": amount, "quote": quote}
    top250 = pd.DataFrame(top250, columns=["rank", "name", "star", "amount", "quote"])
    top250.to_csv("top250.csv", encoding="utf_8_sig", index=False)

def main():
    offsets = [x * 25 for x in range(0, 11)]
    for offset in offsets:
        source = get_page(offset)
        info = get_info(source)
        save_info(info)
main()
