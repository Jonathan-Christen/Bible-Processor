# By Jonathan Christen
import sys
from curses.ascii import isdigit

import requests
from bs4 import BeautifulSoup
import os
import time
from BibleDotComWriterConfig import *

class BibleDotComWriter:
    ''' Gets bible.com data for a bible version and writes it to files. '''
    def __init__(self) -> None:
        ''' Constructor '''
        # Pushes variables from BibleDotComWriterConfigSpanish.py into
        self.url_replace_bible_number = url_replace_bible_number
        self.url_replace_bible        = url_replace_bible
        self.url_replace_book         = url_replace_book
        self.url_replace_chapter      = url_replace_chapter
        self.url_base                 = url_base
        self.books_table              = books_table
        self.chapter_language         = chapter_language
    
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
                if  processed_string[-1] in [ ' ' ]:
                    processed_string = processed_string + verse
                    continue
                
                if verse[0] in [ ' ' ]:
                    processed_string = processed_string + verse
                    continue
                
                if verse[0] in [ ';', ':', ',', '.', '?', '!' ]:
                    processed_string = processed_string + verse
                    continue

                if  verse == 'eñor':
                    processed_string = processed_string + verse
                    continue

                processed_string = processed_string + " " + verse

        # No chapter case.
        if processed_string == None:
            return str()
        
        return processed_string.split("</path></svg>")[-1]

    def _get_book_title(self,book_row: str, site_bible_num: int) -> None:
        ''' Pulls book title from html. '''
        url = self._build_url(book_row, 1, site_bible_num)

        for i in range(10):
            try:
                time.sleep(0.1)
                response = requests.get(url)

                html = response.text
                html = BeautifulSoup(html, "html.parser")
                self.chapter_title = str(html)

                chapter_title_start = '<div class="ChapterContent_reader__Dt27r"><h1>'
                chapter_title_end   = '</h1>'

                self.chapter_title = self.chapter_title.split(chapter_title_start)[-1]
                self.chapter_title = self.chapter_title.split(chapter_title_end)[0]

                while True:
                    if isdigit(self.chapter_title[-1]) == True:
                        self.chapter_title = self.chapter_title[:-2]
                    else:
                        break
                break
            except:
                continue

    def _language(self, language: str) -> None:
        ''' Returns table of bible book tables in a specific language. '''
        print(language)
        if language == "Arabic" or language ==  "arabic":
            self.language  = "arabic"
            return None
        if language == "Spanish" or language == "spanish" or \
           language == "Español" or language == "español":
            self.language  = "spanish"
            return None
        if language == "English" or language == "english":
            self.language  = "english"
            return None
        print("Error: Your language <{0}> is not supported".format(language))
        sys.exit()

    def _build_url(self, book_row: str, chapter_num: str, site_bible_num: int) -> str:
        url = self.url_base                                           \
            .replace(self.url_replace_bible, self.bible.capitalize()) \
            .replace(self.url_replace_book, book_row)                 \
            .replace(self.url_replace_chapter, str(chapter_num))      \
            .replace(self.url_replace_bible_number, str(site_bible_num))
        return url

    def write_bible(self, site_bible_num: int, bible: str, language: str) -> None:
        '''
        Writes bible by chapter to file in a directory named after the bible.

        Parameters
        ----------
            site_bible_num: int
                The bible number in the Bible.com url. Each bible version has its own number.
            bible: str
                This is the bible to be pulled from bible.com and writen to files
                using the bible version's acronym (i.e. kjv, nav, nbla).
            language: str
                The language that is desired to be used.
        '''
        self._language(language)
        if len(self.books_table) == 0:
            return None
        
        self.bible = bible
        self._make_directory()

        # Bible level.
        print("Comenzar | Biblia   | {0}".format(self.bible))
        # Book level.
        for book_row in self.books_table:
            self._get_book_title(book_row, site_bible_num)
            print("Comenzar | Libre    | {0}".format(self.chapter_title))
            book = ""
            chapter_num = 0

            # Chapter level.
            found = True
            while found == True:
                chapter_num += 1
                url = self._build_url(book_row, chapter_num, site_bible_num)
                # Give a multiple tries to get the chapter.
                for i in range(10):
                    try:    
                        # Sometimes pulling information to quickly triggers server in the web server.
                        time.sleep(0.1)
                        response = requests.get(url)
                    except:
                        continue

                    if response.status_code == 200:
                        chapter = self._process_html(response)
                        if len(chapter) > 0:
                            book = book + "{0} {1}\n".format(\
                                self.chapter_language[self.language], str(chapter_num))
                            book = book + chapter + "\n"
                            break
                        else:
                            continue
                    else:
                        print("Error: Failed to retrieve the page {0}. Status code:{1}"\
                            .format(url, response.status_code))
                        continue
                    
                if i == 9:
                    found = False                        
                print("Completo | {0} | {1}".format(
                    self.chapter_language[self.language], str(chapter_num)))
            filename = self.bible + "/" + self.chapter_title + ".txt"
            self._write(book, filename)
        print('Done.')

if __name__ == "__main__":
    bible_class = BibleDotComWriter()
    bible_class.write_bible(103, "nbla", "Spanish")
    bible_class.write_bible(104, "ncv",  "English")
    bible_class.write_bible(101, "keh",  "Arabic")

