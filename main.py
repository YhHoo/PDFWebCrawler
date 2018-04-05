import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.request import urlopen


# return redirected address if they redirect
def check_redirect(url_to_go):
    r = requests.get(url_to_go)
    if r.history:
        print("Request was redirected")
        for resp in r.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(r.status_code, r.url)
        return r.url
    else:
        print("Request was not redirected")
        return None


# From DOI to redirected website to crawl the sci direct url
doi_head = 'http://doi.org/'
doi = '10.1016/j.watres.2018.01.037'
url = doi_head + doi
print('CRAWLING >>> [{}]'.format(url))
response_1 = requests.get(url)
response_in_text = response_1.text
soup_1 = BeautifulSoup(response_in_text, 'lxml')
tag = soup_1.find('input', attrs={'name': 'redirectURL'})
# unquote convert the unwanted symbol to url symbol
sci_dir_url = unquote(tag['value'])
print('CRAWLING >>> [{}]'.format(sci_dir_url))

# from the sci direct url crawl the pdf file
response_2 = requests.get(sci_dir_url)
response_in_text = response_2.text
soup_2 = BeautifulSoup(response_in_text, 'lxml')
tag = soup_2.find('meta', attrs={'name': 'citation_pdf_url'})
pdf_url = tag['content']
print('CRAWLING >>> [{}]'.format(pdf_url))

# access into pdf
response_3 = requests.get(pdf_url)
# save to local disk
with open('PDF_1.pdf', 'wb') as f:
    f.write(response_3.content)


