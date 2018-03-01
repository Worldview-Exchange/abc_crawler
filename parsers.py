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

import requests
response = requests.get("http://www.abc.net.au/news/2018-03-01/south-africa-plan-to-best-australia-keep-steve-smith-quiet/9498062?section=sport")
parser = ArticleParser()
parser.feed(str(response.content))