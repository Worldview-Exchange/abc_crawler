import requests
import pandas as pd
from parsers import *

# Extract set of articles of a specified topic
def crawlTopic(topic, num_articles):
    parser = TopicParser()
    page = 1
    
    while True:
        # collect topic page and extract article links
        response = requests.get("http://www.abc.net.au/news/topic/%s" % topic)
        parser.feed(str(response.content))

        # handle page increment
        page += 1
        topic += "?page=%d" % page

        # exit loop when enough article links have been extractedcr
        if len(parser.articles) > num_articles:
            break

    return parser.articles[:num_articles]

# Get article content for list of article links
def crawlArticles(article_links):
    articles = []
    parser = ArticleParser()
    for article in article_links:
        response = requests.get("http://www.abc.net.au%s" % article)
        parser.feed(str(response.content))
        articles.append(parser.retrieve_article())

    return [article for article in articles if article.content != ""]

# Output article content to a csv file
def outputToCsv(articles, file_name):
    df = pd.DataFrame([vars(x) for x in articles], columns=['title', 'date', 'description', 'content', 'topics'])
    df.to_csv(file_name)

# Get set of articles that are similar to a given article
def get_similar_articles(article, num_articles=10, similarity=0.5):
    # define necessary number of shared topics
    sim_threshold = int(len(article.topics)*similarity)

    articles = []
    for topic in article.topics:
        [articles.append(x) for x in crawlTopic(topic, num_articles)]

    crawled = crawlArticles(articles)
    similar = [x.topics for x in crawled if len(set(x.topics).intersection(article.topics)) >= sim_threshold]
    similar.sort(key=lambda x: len([y for y in x if y in article.topics]))
    return similar[-num_articles:]
