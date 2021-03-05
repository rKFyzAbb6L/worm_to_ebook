from worm_to_ebook.webserial_utils import get_book
from worm_to_ebook.epub_utils import make_epub
from ebooklib import epub


if __name__ == "__main__":
    worm_book = get_book('https://parahumans.wordpress.com' +
                         '/category/stories-arcs-1-10/arc-1-gestation/1-01/')
    worm_epub = make_epub(worm_book)
    epub.write_epub('worm_by_jc_mcrae.epub', worm_epub, {})
