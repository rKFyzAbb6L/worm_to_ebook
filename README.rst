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

    # chapter refs all seem to be nested in <div class="entry-content"> in the <article> tag
    # so find all the href in tags that are descendents of <div class="entry-content">
    # divs don't seem to be included in .descendants. seems related to how html.parser parse the page.
    # lxml does OK.

https://parahumans.wordpress.com/2017/11/02/glow-worm-p-7/   
https://parahumans.wordpress.com/2017/11/04/glow-worm-p-8/        
https://parahumans.wordpress.com/2017/11/07/glow-worm-p-9/   
https://parahumans.wordpress.com/table-of-contents/?share=twitter
https://parahumans.wordpress.com/table-of-contents/?share=facebook