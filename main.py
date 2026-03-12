import requests
import pandas as pd
import json

DATA_DIR = "data"

def load_products():
  products = []
  for file in DATA_DIR.glob("*.json"):
    with open(file, encoding="utf-8") as f:
      data = json.load(f)
    products.extend(data["products"])
  return products
  

def parse_product(p):
  article = p["id"]
  price = p["sizes"][0]["price"]["product"] / 100
  sizes = [s["name"] for s in p["sizes"]]

  return {
    "link": f"https://www.wildberries.ru/catalog/{article}/detail.aspx",
    "article": article,
    "name": p["name"],
    "price": price,
    "seller": p["supplier"],
    "seller_link": f"https://www.wildberries.ru/seller/{p['supplierId']}",
    "sizes": ",".join(sizes),
    "stock": p.get("totalQuantity", 0),
    "review_rating": p.get("reviewRating", 0),
    "reviews": p.get("feedbacks", 0),
    "total_quantity": p.get("totalQuantity", 0)
    # Ссылки на картинки, описание и характеристики не стал вставлять, так как для этого надо проваливаться в каждую карточку
  }


query = "пальто из натуральной шерсти"
# Непосредственно по этой ссылке удалось получить JSON только вручную через браузер
url = f"https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?ab_testing=false&appType=1&curr=rub&dest=-1255987&f14177451=15000203&hide_vflags=4294967296&inheritFilters=false&lang=ru&page=1&priceU=41800%3B1000000&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"

response = requests.get(url)
data = response.json()

products = data.get("products", [])

catalog = []

for p in products:
  catalog.append(parse_product(p))

df = pd.DataFrame(catalog)
filtered = df[
  (df["rating"] >= 4.5)
]

filtered.to_excel("filtered_catalog.xlsx", index=False)
