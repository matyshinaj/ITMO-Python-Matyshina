import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    comment_list = []
    tr = parser.find_all('tr', {'class': 'athing'})
    url = parser.find_all('a', {'class': 'storylink'})
    td = parser.find_all('td',{'class': 'subtext'})
    for n in range(len(tr)):
        comment = td[n].find_all('a')[(len(td[n].find_all('a')))-1].text
        if comment == 'discuss'or comment == 'hide':
            comment = '0\xa0comments'
        elif comment == '1\xa0comment':
            comment = '1\xa0comments'
        comment_list.append(comment)
        points = td[n].span.text.split()[0]
    for i in range(len(tr)):
        news = {
            'title': url[i].text,
            'author': (td[i].find_all('a'))[0].text,
            'url': url[i]['href'],
            'comments': comment_list[i][:-9],
            'points': points,
        }
        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_page ='?' + parser.find('a',{'class': 'morelink'})['href'].split('?')[1]
    return next_page




def get_news(url, n_pages=34):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/newest" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


