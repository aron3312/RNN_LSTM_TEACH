import requests
import pickle
from lxml import etree
import re
import pandas as pd
from datetime import datetime

class Ltn_crawler(object):
    def __init__(self):
        self.url = "http://news.ltn.com.tw/list/newspaper/"
        self.category = self.get_allcategory()
    def request_url(self,url):
        req = requests.get(url)
        content = req.content.decode("UTF-8")
        html = etree.HTML(content)
        return html
    def get_allcategory(self):
        html = self.request_url(self.url)
        cat_class = html.xpath("/html/body/div[3]/section/ul/li")
        cat = dict([(re.sub(r'.*newspaper/([^/]+).*',r'\1', p.xpath('a/@href')[0]),p.xpath('a/@data-desc')[0]) for p in cat_class][1:])
        return cat
    def crawl_page(self,date,all_reuslt):
        all_categories = dict([k for k in self.category.items() if k[0] in ['politics','society','business','sports']])
        print(all_categories)
        for category in all_categories:
            html = self.request_url(self.url+category+'/'+date)
            print(self.url+category+'/'+date)
            [all_reuslt.append((category,re.sub('\s','',p))) for p in html.xpath('//*[@class="list"]/li/a[2]/p/text()')]




if __name__ == '__main__':
    crawler = Ltn_crawler()
    print(crawler.category)
    all_result = []
    date_range = [datetime.strftime(x,'%Y%m%d') for x in list(pd.date_range(start="20171101", end="20171231"))]
    for date in date_range:
        crawler.crawl_page(date,all_result)
    print(len(all_result))
    pickle.dump(all_result,open('dataset3.pkl','wb'))

