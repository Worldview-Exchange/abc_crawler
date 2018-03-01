import requests
from parsers import *

# response = requests.get("http://www.abc.net.au/news/2018-03-01/south-africa-plan-to-best-australia-keep-steve-smith-quiet/9498062?section=sport")
# parser = ArticleParser()
# parser.feed(str(response.content))

response = requests.get("http://www.abc.net.au/news/topic/winter-olympics")
parser = TopicParser()
parser.feed(str(response.content))