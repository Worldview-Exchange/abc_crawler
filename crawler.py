import requests
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

        # exit loop when enough article links have been extracted
        if len(parser.articles) > num_articles:
            break

    return parser.articles[:num_articles]

articles = crawlTopic("winter-olympics", 26)

article_content = []
for article in articles:
    response = requests.get("http://www.abc.net.au%s" % article)
    parser = ArticleParser()
    parser.feed(str(response.content))
    article_content.append(parser.content)

print(articles[0] + "\n")
print(article_content[0])