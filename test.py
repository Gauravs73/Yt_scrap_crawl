
import urllib.request as urllib2
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json




for links in list:

    myurl = "https://www.youtube.com"
    url1=urljoin(myurl,links)
    page = urllib2.urlopen(url1)
    list = []
    soup = BeautifulSoup(page)
    html_content_bytes = str(soup).encode("utf-8")
    html_content_str = html_content_bytes.decode("utf-8")
    url_count = html_content_str.count('''"url":''')
    print("url_count: ", html_content_str.count('''"url":'''))


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
            # print('ind: ', ind)
            ind1 = ind + ind1
            # print('ind1: ',ind1)
            # i = i+1
            # print(i)
            # print(url_returned)
            if url_returned not in list:
                list.append(url_returned)


        except:
            print('error received hence breaking')
            break

print(list)


