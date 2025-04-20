# By Jonathan Christen
import sys
import requests
from bs4 import BeautifulSoup
import os   
import time
from BibleDotComWriterConfigSpanish import *

class BibleDotComWriter:
    ''' Gets bible.com data for a bible version and writes it to files. '''
    def __init__(self) -> None:
        ''' Constructor '''
        # Pushes variables from BibleDotComWriterConfigSpanish.py into
        self.url_replace_bible   = url_replace_bible
        self.url_replace_book    = url_replace_book
        self.url_replace_chapter = url_replace_chapter
        self.url_base            = url_base
        self.books_table         = books_table
    
    def __del__(self) -> None:
        ''' Deconstructor '''
        return None
    
    def _write(self, data: str, filename: str) -> None:
        ''' Write data to a file. '''
        f = open(filename, "w", encoding='utf-8')
        f.write(data)
        f.close()

    def _make_directory(self) -> None:
        ''' Make a new directory. '''
        if not os.path.exists(self.bible):
            os.mkdir(self.bible)

    def _process_html(self, response):
        ''' Processes html page data. '''

        # Prepare HTML text.
        html = response.text
        html = BeautifulSoup(html, "html.parser")
        text = str(html)

        # Parsing strings in the HTML.
        verse_number_start = "R2PLt\">"
        verse_start        = "RrUqA\">"
        end                = "</span>"

        # Split text to first verse.
        verse_numbers = text.split(verse_number_start)
        processed_string = None
        for count, raw in enumerate(verse_numbers):
            # Verses 0 and 1 are unusable values.
            if count < 2:
                continue

            # Gather Verses
            verses_raw = raw.split(verse_start)
            for verse in verses_raw:
                verse = verse.split(end)[0]
                
                # The # occurs within verse continuation.
                if verse == '#':
                    continue

                # First use.
                if processed_string == None:
                    processed_string = verse
                    continue

                # Edge cases.
                if  processed_string[-1] in [ ' ' ] or\
                    verse[0]             in [ ' ' ] or\
                    processed_string[-1].isalpha() and verse[0] in \
                        [ ':', ',', '.', '?', '!' ]:
                    processed_string = processed_string + verse
                    continue
                
                if processed_string[-1].isalpha() and verse[0] in [':',',','.']:
                    processed_string = processed_string + verse
                    continue

                if  verse == 'eñor':
                    processed_string = processed_string + verse
                    continue

                processed_string = processed_string + " "  + verse
        
        # No chapter case.
        if processed_string == None:
            return str()
        
        return processed_string.split("</path></svg>")[-1]
        
    def write_bible(self, bible: str) -> None:
        '''
        Writes bible by chapter to file in a directory named after the bible.

        Parameters
        ----------
            bible: str
                This is the bible to be pulled from bible.com and writen to files
                using the bible version's acronym (I.E. KJV, NAV, NBLA).
        '''
        self.bible = bible
        self._make_directory()
        # Bible level.
        print("Comenzar | Biblia   | {0}".format(self.bible))
        # Book level.
        for book_row in self.books_table:
            print("Comenzar | Libre    | {0}".format(book_row[0]))
            book = ""
            chapter_num = 0
            # Chapter level.
            while True:
                chapter_num += 1
                url = (self.url_base.replace(self.url_replace_bible,   self.bible))    \
                                    .replace(self.url_replace_book,    book_row[1]) \
                                    .replace(self.url_replace_chapter, str(chapter_num))
                
                try:
                    # Sometimes pulling information to quickly triggers server in the web server.
                    time.sleep(0.5)
                    response = requests.get(url)
                except:
                    break
                
                if response.status_code == 200:
                    chapter = self._process_html(response)
                    if len(chapter) > 0:
                        book = book + "Capitulo {0}\n".format(str(chapter))
                        book = book + chapter + "\n"
                    else:
                        break
                else:
                    print("Error: Failed to retrieve the page {0}. Status code:{1}"\
                          .format(url, response.status_code))
                    continue
                print("Completo | Capitulo | {0}".format(str(chapter_num)))
            filename = self.bible + "/" + book_row[0] + ".txt"
            self._write(book, filename)
        print('Done.')

if __name__ == "__main__"():
    bible_class = BibleDotComWriter()
    bible_class.write_bible("nbla")