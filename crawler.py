import requests
from parsers import *

def crawlTopic(topic, num_articles):
    parser = TopicParser()
    page = 1
    
    while True:
        response = requests.get("http://www.abc.net.au/news/topic/%s" % topic)
        parser.feed(str(response.content))

        page += 1
        topic += "?page=%d" % page

        if len(parser.articles) > num_articles:
            break

    print(parser.articles[:num_articles])

# response = requests.get("http://www.abc.net.au/news/2018-03-01/south-africa-plan-to-best-australia-keep-steve-smith-quiet/9498062?section=sport")
# parser = ArticleParser()
# parser.feed(str(response.content))

crawlTopic("winter-olympics", 26)