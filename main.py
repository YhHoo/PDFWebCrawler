import requests
import re
import codecs
from pandas import DataFrame, read_csv
from bs4 import BeautifulSoup
from urllib.parse import unquote
from urllib.request import urlopen
import bibtexparser

# l = ['asd', 'sda', 'shd']
# df = DataFrame(data=l)
# print(df)

# with codecs.open('C://Users//YH//Desktop//scopus.bib', 'r', errors='replace', encoding='utf-8') as bib_file:
#     doi_list = []
#     for line in bib_file:
#         if line[0:3] == 'doi':
#             doi = re.sub('[{},]', '', line[4:])
#             doi_list.append(doi.strip())
#
# df = DataFrame(data=doi_list)
# df.to_csv('DOI_List_p1.csv')


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


def search_save_pdf(doi, save_dir=None):
    # From DOI to redirected website to crawl the sci direct url
    doi_head = 'http://doi.org/'
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
    print(response_in_text)
    soup_2 = BeautifulSoup(response_in_text, 'lxml')
    tag = soup_2.find('meta', attrs={'name': 'citation_pdf_url'})
    pdf_url = tag['content']
    print('CRAWLING >>> [{}]'.format(pdf_url))

    # crawl secure pdf link
    response_3 = requests.get(pdf_url)
    response_in_text = response_3.text
    soup_3 = BeautifulSoup(response_in_text, 'lxml')
    tag = soup_3.find('a')
    pdf_url_secure = tag['href']
    print('SAVING >>> [{}]\n'.format(pdf_url_secure))

    # # access into pdf and save
    # response_3 = requests.get(pdf_url_secure)
    # # save to local disk
    # with open('PDF_1.pdf', 'wb') as f:
    #     f.write(response_3.content)


# Do the extraction
# df = read_csv('DOI_List_p1.csv', index_col=0)
# df = df.values
# for doi in df:
#     search_save_pdf(doi=doi[0])

search_save_pdf(doi='10.1016/j.jclepro.2018.01.239')
