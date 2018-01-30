import urllib3
import certifi
import re
from bs4 import BeautifulSoup as bs

html = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

ii = 0
while ii < 100:#318180:
    r = html.request('GET', 'https://www.chefkoch.de/rs/s{:d}g0/'.format(ii))
    soup = bs(r.data, 'lxml')
    listItems = soup.find_all('li')
    for li in listItems:
        if 'class' in li.attrs:
            if 'search-list-item' in li.attrs['class']:
                print(ii)
                index = int(li.attrs['id'][7:])
                r = html.request('GET', 'https://www.chefkoch.de/rezepte/{:d}'.format(index))
                soup = bs(r.data, 'lxml')
                for script in soup.find_all('script'):
                    if script.text.find('_simplora_params.recipes') >= 0:
                        rec = re.findall('_simplora_params.recipes.push\({(.*?)}\);', script.text, re.DOTALL)[0]
                        rec = re.sub('\n', '', rec)
                ii += 1