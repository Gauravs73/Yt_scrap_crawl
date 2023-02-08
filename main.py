import logging
from urllib.parse import urljoin
import requests
import json
from bs4 import BeautifulSoup
import urllib.request as urllib2

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

url_list=[]
channel_ids=[]
class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        page= urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        html_content_bytes = str(soup).encode("utf-8")
        html_content_str = html_content_bytes.decode("utf-8")
        url_count = html_content_str.count('''"url":''')

        def find_url(text_file):
            sub1 = '''/watch?v='''
            sub2 = '''","webPageType":'''

            # getting index of substrings
            idx1 = text_file.index(sub1)
            idx2 = text_file[idx1:].index(sub2)
            return (text_file[idx1:idx1 + idx2], idx1 + idx2)

        ind1 = 0
        # i = 0
        while True:
            try:
                url_returned, ind = find_url(html_content_str[ind1:])

                ind1 = ind + ind1

                path = urljoin(url, url_returned)
                yield path
                print(path)
                url_list.append(path)
                if (len(path)>25000):
                    channel_id=path[-25:]
                    if channel_id not in channel_ids:

                        channel_ids.append(channel_id)
                    print(channel_ids)

                else:
                    pass





            except:
                print('error received hence breaking')
                break







    def add_url_to_visit(self, url):

        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)


    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

'''with open('url_listjs', 'r+') as f:
    data=json.load(f)
    data.append(url_list)
    f.seek(0)
    json.dump(data,f)'''



if __name__ == '__main__':
    Crawler(urls=['https://www.youtube.com/']).run()


