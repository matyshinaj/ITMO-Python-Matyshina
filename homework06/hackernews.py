from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    id = request.query.id
    label = request.query.label
    s = session()
    news = s.query(News).filter(News.id == id).first()
    news.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest", n_pages=30)
    s = session()
    for i in news:
        if s.query(News).filter(News.title == i['title'], News.author == i['author']).first():
            break
        else:
            s.add(News(**i))
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier.fit(x_train, y_train)

    news = s.query(News).filter(News.label == None).all()
    for one in news:
        [prediction] = classifier.predict([clean(one.title)])
        if prediction == 'good':
            good.append(one)
        elif prediction == 'maybe':
            maybe.append(one)
        else:
            never.append(one)

    return template('news_recommendations', good=good, maybe=maybe, never=never)


if __name__=="__main__":
    s = session()
    labeled_news = s.query(News).filter(News.label != None).all()
    x_train = [clean(news.title) for news in labeled_news]
    y_train = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier()
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)

