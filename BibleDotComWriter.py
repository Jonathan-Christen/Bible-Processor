'''
    Jonathan Christen
    2025
'''
from curses.ascii import isdigit
import requests
from bs4 import BeautifulSoup
import os
import time
from BibleDotComWriterConfig import *

class BibleDotComWriter:
    '''
    Gets a bible from bible.com using their numbering system and writes each book
    of the bible to a file from that version.
    '''
    def __init__(self) -> None:
        '''
        Constructor
        '''
        # Pushes variables from BibleDotComWriterConfig.py into the object.
        self._url_replace_bible_number = url_replace_bible_number
        self._url_replace_bible        = url_replace_bible
        self._url_replace_book         = url_replace_book
        self._url_replace_chapter      = url_replace_chapter
        self._url_base                 = url_base
        self._books_table              = books_table
        self._language_specific        = language_specific
        self._parser_data              = parser_data

    def __del__(self) -> None:
        '''
        Deconstructor
        '''
        return None

    def _write(self, data: str, filename: str) -> None:
        '''
        Write data to a file.

        Parameters
        ----------
        data : str
            Data to be written as a string.
        filename : str
            Name of the file to write to.
        '''
        f = open(filename, "w", encoding='utf-8')
        f.write(data)
        f.close()

    def _make_directory(self) -> None:
        '''
        Make a new directory for each bible version.
        '''
        if not os.path.exists(self._bible):
            os.mkdir(self._bible)

    def _process_html(self, response: object) -> str:
        '''
        Processes HTML page data.

        Parameters
        ----------
        response : object
            HTML output from requests.

        Returns
        -------
        chapter : str
            Processed chapter with all html wrappers removed.
        '''
        # Prepare HTML text.
        html = response.text
        html = BeautifulSoup(html, "html.parser")
        text = str(html)

        # Split text to first verse.
        verse_numbers = text.split(self._parser_data['verse_number_start'])
        processed_string = None
        for count, raw in enumerate(verse_numbers):
            # Verses 0 and 1 are unusable values.
            if count < 2:
                continue

            # Gather verses.
            verse_raw = raw.split(self._parser_data['verse_start'])
            for verse_section in verse_raw:
                verse_section = verse_section.split(self._parser_data['verse_end'])[0]

                # The # is used for site links
                if verse_section == '#':
                    continue

                # First string case.
                if processed_string == None:
                    processed_string = verse_section
                    continue

                # Edge cases.
                if  processed_string[-1] in [ ' ', '(' ]:
                    processed_string = processed_string + verse_section
                    continue

                if verse_section[0] in [ ' ', ';', ':', ',', '.', '?', '!' ]:
                    processed_string = processed_string + verse_section
                    continue

                if  verse_section == 'eñor':
                    processed_string = processed_string + verse_section
                    continue

                if  processed_string[-1] == 'L' and verse_section[:3] == 'ord':
                    processed_string = processed_string + verse_section
                    continue

                processed_string = processed_string + " " + verse_section

        # No chapter case.
        if processed_string == None:
            return str()

        return processed_string.split(self._parser_data['verses_end'])[-1]

    def _get_book_title(self, book: str, site_bible_num: int) -> None:
        '''
        Pulls book title from HTML.

        Parameters
        ----------
            book : str
                Row name for the book.
            site_bible_num : str
                Number for the bible in bible.com (each bible has its own number).
        '''
        url = self._build_url(book, 1, site_bible_num)

        for i in range(10):
            try:
                time.sleep(0.1)
                response = requests.get(url)
                if response.status_code == 200:
                    html = response.text
                    html = BeautifulSoup(html, "html.parser")
                    self._chapter_title = str(html)
                    self._chapter_title = self._chapter_title.split(self._parser_data['chapter_title_start'])[-1]
                    self._chapter_title = self._chapter_title.split(self._parser_data['chapter_title_end'])[0]
                else:
                    continue

                while True:
                    if isdigit(self._chapter_title[-1]) == True:
                        self._chapter_title = self._chapter_title[:-2]
                    else:
                        break
                break
            except:
                if i == 9:
                    print("Chapter title for book {1} could not be aquired.".format(book))
                continue

    def _language(self, language: str) -> None:
        '''
        Returns table of bible book tables in a specific language.

        Parameters
        ----------
        language : str
            Language for of the selected bible.
        '''
        for key, value in self._language_specific.items():
            if language in value['language_icons']:
                self._language = key
                return None
        print("Warning: Your language <{0}> is not supported, switching to english.".format(language))
        self._language = "english"

    def _build_url(self, book: str, chapter_num: str, site_bible_num: int) -> str:
        """
        Builds the URL for the HTML query.

        Parameters
        ----------
        book : str
            Book name.
        chapter_num : str
            Chapter number in the bible verse.
        site_bible_num : int
            Name of the bible version from the site.

        Returns
        -------
        url : str
            url string of the webpage to be queried.
        """
        url = self._url_base                                           \
            .replace(self._url_replace_bible, self._bible.capitalize()) \
            .replace(self._url_replace_book, book)                     \
            .replace(self._url_replace_chapter, str(chapter_num))      \
            .replace(self._url_replace_bible_number, str(site_bible_num))
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
        if len(self._books_table) == 0:
            print("books_table in the config file is empty, {0} not written to file.".format(bible))
            return None

        self._bible = bible
        self._make_directory()

        # Bible (version) level.
        print("{0} {1}".format(self._language_specific[self._language]['version'], self._bible))
        # Book level.
        for book_acronym in self._books_table:
            self._get_book_title(book_acronym, site_bible_num)
            print("{0} {1}".format(self._language_specific[self._language]['book'], self._chapter_title))
            book = ""
            chapter_num = 0

            # Chapter level.
            found = True
            while found == True:
                chapter_num += 1
                url = self._build_url(book_acronym, chapter_num, site_bible_num)
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
                                self._language_specific[self._language]['chapter_header'], str(chapter_num))
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
                print("{0} {1}".format( self._language_specific[self._language]['chapter'], str(chapter_num)))
            filename = self._bible + "/" + self._chapter_title + ".txt"
            self._write(book, filename)
        print('Done.')

# Example code.
if __name__ == "__main__":
    bible_class = BibleDotComWriter()
    #bible_class.write_bible(1588, "amp",  "English")
    bible_class.write_bible(101,  "keh",  "Arabic" )
    bible_class.write_bible(103,  "nbla", "Spanish")

