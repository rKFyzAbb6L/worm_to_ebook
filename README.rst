html.parser doesn't seem to handle empty div or empty p tag, and ends up erroneously closing the parent tag early.

so, use lxml or html5lib. both seem to handle that case on the contents page.

```
from urllib.request import request
from bs4 import BeautifulSoup

with request.urlopen(CONTENTS) as response:
    html_contents = response.read()

soupHtmlParser = BeautifulSoup(html_contents,'html.parser')
soupHtml5lib = BeautifulSoup(html_contents,'html5lib')
soupLxml = BeautifulSoup(html_contents,'lxml')

for x in ['soupLxml','soupHtmlParser','soupHtml5lib']:
 with open('{}.html'.format(x), 'w') as f:
  f.write(globals()[x].prettify())

```