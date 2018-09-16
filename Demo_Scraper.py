from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def process(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    # div=html.select('div')
    for div in (html.select('div')):
        if div.get('id') == 'placardContainer':
            html = div
            for i in html.select('li'):
                temp = i
                for apt_name in temp.findAll('a', {'class': 'placardTitle'}):
                    print(apt_name.text)
                for apt_name in temp.findAll('div', {'class': 'location'}):
                    print(apt_name.text)
                for img_url in temp.findAll('div', {'class': 'item'}):
                    print(img_url.get('title'))
                for apt_rent in temp.findAll('span', {'class': 'altRentDisplay'}):
                    print(apt_rent.text)
                for apt_size in temp.findAll('span', {'class': 'unitLabel'}):
                    print(apt_size.text)
                for apt_avbl in temp.findAll('span', {'class': 'availabilityDisplay'}):
                    print(apt_avbl.text)
                for apt_phone in temp.findAll('div', {'class': 'phone'}, 'span'):
                    print(apt_phone.text.strip())
                for apt_amen in temp.findAll('ul', {'class': 'amenities'}):
                    temp1 = apt_amen
                    for apt_amen in temp1.select('li'):
                        print(apt_amen.get('title'))



start = time.time()

site="https://www.apartments.com/dallas-tx/"
raw_html=simple_get(site)
process(raw_html)

html = BeautifulSoup(raw_html, 'html.parser')
# div=html.select('div')
for a in html.findAll('a', {'class': 'next'}):
    print("\n \n Next Page:",a.get('data-page'))
    site=site+a.get('data-page')
    raw_html = simple_get(site)
    process(raw_html)

stop= time.time()
print("Duration:", stop-start)