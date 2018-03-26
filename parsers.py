from html.parser import HTMLParser

class Article:
    def __init__(self, title=""):
        self.title = title
        self.content = ""
        self.description = ""
        self.date = ""
        self.topics = []

# Parse content from an article page
class ArticleParser(HTMLParser):
    intitle = False
    indiv = False
    inp = False
    intopics = False
    attopic = False
    nesting = 0
    article = Article()

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if attrs and attrs[0][1] == "article section":
                self.indiv = True
                self.nesting = 1
            elif self.indiv:
                self.nesting += 1
        elif tag == "p" and not attrs and self.indiv:
            self.inp = True
        elif tag == "h1":
            self.intitle = True
        elif tag == "meta":
            if attrs and attrs[0][1] == "description":
                self.article.description = attrs[1][1]
            elif attrs and attrs[0][1] == "og:updated_time":
                self.article.date = attrs[1][1]
        elif tag == "p":
            if attrs and attrs[0][1] == "topics":
                self.intopics = True
        elif tag == "a" and self.intopics:
            self.attopic = True

    def handle_data(self, data):
        if self.inp:
            self.article.content += data.encode().decode('unicode_escape') + " "
        elif self.intitle:
            self.article.title += data
        elif self.intopics and self.attopic:
            self.article.topics.append(data)

    def handle_endtag(self, tag):
        if tag == "div" and self.indiv:
            if self.nesting == 0:
                self.indiv = False
            else:
                self.nesting -= 1
        elif tag == "p" and self.indiv and self.inp:
            self.inp = False
            self.article.content += "\n"
        elif tag == "h1":
            self.intitle = False
        elif tag == "p" and self.intopics:
            self.intopics = False
        elif tag == "a" and self.attopic:

            self.attopic = False

    # Returns current article and resets object for next parse
    def retrieve_article(self):
        # reset parser article
        article = self.article
        self.article = Article()

        # remove unicode from article content
        import string
        printable = set(string.printable)
        article.content = "".join(filter(lambda x: x in printable, article.content))

        return article

# Parse list of articles from a topic page
class TopicParser(HTMLParser):
    inlist = False
    initem = False
    is_media = False

    current_article = ""
    articles = []

    def handle_starttag(self, tag, attrs):
        if tag == "ul":
            if attrs and attrs[0][1] == "article-index":
                self.inlist = True
        elif tag == "h3" and self.inlist:
            self.initem = True
        elif tag == "a" and self.initem:
            if attrs:
                self.current_article = attrs[0][1]
        if tag == "span" and self.initem:
            # trigger marker for media content
            if attrs and attrs[0][1] == "type":
                self.is_media = True

    def handle_endtag(self, tag):
        if self.inlist:
            if tag == "ul":
                self.inlist = False
            elif tag == "h3":
                # if not a media or broken article then add to list
                if not self.is_media and self.current_article != "":
                    print("%d: %s" % (len(self.articles), self.current_article))
                    self.articles.append(self.current_article)

                # reset markers
                self.is_media = False
                self.initem = False