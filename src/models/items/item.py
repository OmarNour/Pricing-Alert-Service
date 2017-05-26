import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=0.00, _id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name,self.url)

    def load_price(self):
        # Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">$449.00</span>
        # https://www.amazon.com/dp/B01CO2JPYS/ref=s9_acsd_bw_wf_e_FD2017WF_cdl_10?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-15&pf_rd_r=010KZ3ZFTW9T0W0MFFF5&pf_rd_t=101&pf_rd_p=8a015a11-87a6-4e37-b2b0-27d4532fdb7c&pf_rd_i=502661011
        # Zopella:
        # <div class="detail-price" itemprop="price"><span class="price">LE 2,249.00</span></div>
        # <span class="price">LE 2,249.00</span>
        request = requests.get(self.url)
        content = request.content

        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()
        pattern = re.compile("(\d+.\d+)")

        match = pattern.search(string_price)
        self.price = float(match.group().replace(",", ""))

        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {"name": self.name,
                "url": self.url,
                "price": float(self.price),
                "_id": self._id}

    @classmethod
    def get_from_mango(cls,url):
        item = Database.find_one(ItemConstants.COLLECTION, {'url': url})
        return cls(**item)

    @classmethod
    def get_by_id(cls,item_id):
        item = Database.find_one(ItemConstants.COLLECTION, {'_id': item_id})
        return cls(**item)
