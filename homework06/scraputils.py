import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    comment_list = []
    tr = parser.find_all('tr', attrs={'class': 'athing'})
    url = parser.find_all('a', attrs={'class': 'storylink'})
    points = parser.find_all('span', attrs={'class': 'score'})
    author = parser.find_all('a', attrs={'class': 'hnuser'})
    comments = parser.find_all('td', attrs={'class': 'subtext'})
    for n in range(0, len(comments)):
        comment = comments[n].find_all('a')[3].text
        if comment == 'discuss':
            comment = '0\xa0comments'
        elif comment == '1\xa0comment':
            comment = '1\xa0comments'
        else:
            comment = comments[n].find_all('a')[3].text
        comment_list.append(comment)
    for i in range(len(tr)):
        news = {
            'title': url[i].text,
            'author': author[i].text,
            'url': url[i]['href'],
            'comments': comment_list[i][:-9],
            'points': points[i].text[:-7],
        }
        news_list.append(news)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_page = parser.find_all('a',attrs = {'class': 'morelink'})['href']
    return next_page




def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

