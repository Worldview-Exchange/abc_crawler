from html.parser import HTMLParser

# Parse content from an article page
class ArticleParser(HTMLParser):
    indiv = False
    inp = False
    nesting = 0
    content = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if attrs and attrs[0][1] == "article section":
                self.indiv = True
                self.nesting = 1
            elif self.indiv:
                self.nesting += 1
        elif tag == "p" and not attrs and self.indiv:
            self.inp = True

    def handle_data(self, data):
        if self.inp:
            self.content = self.content + " " + data.encode().decode('unicode_escape')

    def handle_endtag(self, tag):
        if tag == "div" and self.indiv:
            if self.nesting == 0:
                self.indiv = False
                print(self.content)
            else:
                self.nesting -= 1
        elif tag == "p" and self.indiv:
            self.inp = False

# Parse list of articles from a topic page
class TopicParser(HTMLParser):
    inlist = False
    initem = False
    articles = []

    def handle_starttag(self, tag, attrs):
        if tag == "ul":
            if attrs and attrs[0][1] == "article-index":
                self.inlist = True
        elif tag == "h3" and self.inlist:
            self.initem = True
        elif tag == "a" and self.initem:
            if attrs:
                self.articles.append(attrs[0][1])

    def handle_data(self, data):
        True

    def handle_endtag(self, tag):
        if self.inlist:
            if tag == "ul":
                self.inlist = False
            elif tag == "h3":
                self.initem = False
