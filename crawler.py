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

        # exit loop when enough article links have been extracted
        if len(parser.articles) > num_articles:
            break

    return parser.articles[:num_articles]

def crawlArticles(article_links):
    article_content = []
    for article in article_links:
        response = requests.get("http://www.abc.net.au%s" % article)
        parser = ArticleParser()
        parser.feed(str(response.content))
        article_content.append(parser.content)

    return article_content

def outputToPdf(articles, file_name):
    df = pd.DataFrame(articles, columns=["content"])
    df.to_csv(file_name)


import sys, getopt

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:n:o:",["topic=","num=","ofile="])
   except getopt.GetoptError:
      print('crawler.py -i <topic> -n <number_of_articles> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('crawler.py -i <topic> -n <number_of_articles> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--topic"):
         topic = arg
      elif opt in ("-n", "--num"):
          # TODO: handle type incompatibility
         num = int(arg)
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Crawling %d articles from topic \"%s\"...' % (num, topic))
   topic = crawlTopic(topic, num)
   articles = crawlArticles(topic)
   print('Writing files to %s...' % outputfile)
   outputToPdf(articles, outputfile)
   print("Done...")


if __name__ == "__main__":
   main(sys.argv[1:])