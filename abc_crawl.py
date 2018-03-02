import sys, getopt
from crawling import *

def main(argv):
    # handle sys arguments
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

    # crawl articles for topic 
    print('Crawling %d articles from topic \"%s\"...' % (num, topic))
    topic = crawlTopic(topic, num)
    articles = crawlArticles(topic)

    # writes articles to file
    print('Writing files to %s...' % outputfile)
    outputToPdf(articles, outputfile)
    print("Done...")


if __name__ == "__main__":
   main(sys.argv[1:])