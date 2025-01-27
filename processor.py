# By Jonathan Christen

import requests
from bs4 import BeautifulSoup
import os   
from inputs import *

class SourceGetter:
    ''' Gets website data and writes it to files. '''
    
    def __init__(self):
        ''' Constructor '''
        return None
    
    def __del__(self):
        ''' Deconstructor '''
        return 0
    
    def write(self, data, filename):
        ''' Write book '''
        f = open(filename, "w", encoding='utf-8')
        f.write(data)
        f.close()
        return 0

    def make_directory(self, directory):
        if os.path.exists(directory):
            return 0
        else:
            os.mkdir(directory)
        return 0

    def process_html(self, response):
        ''' processes html '''
        
        html = response.text
        html = BeautifulSoup(html, "html.parser")
        text = str(html)
        
        number_start = "R2PLt\">"
        verse_start = "RrUqA\">"
        end   = "</span>"

        verse_numbers = text.split(number_start)
        processed_string = ""
        for count, raw in enumerate(verse_numbers):
            # Index 0 and 1 are junk values.
            if count < 2:
                continue
            
            verses_raw = raw.split(verse_start)
            for verse in verses_raw:
                verse = verse.split(end)[0]
                
                # The # occurs within verse continuation.
                if verse == '#':
                    continue
                
                if len(processed_string) != 0:
                    if processed_string[-1].isdigit():
                        processed_string = processed_string + " "  + verse
                        continue
                processed_string = processed_string + verse 
        
        return processed_string.split("</path></svg>")[-1]
        
    def pull_html_data(self):
        ''' '''
        for row in table:
            book = ""
            go  = True
            index = int(0)
            while go == True:
                index += 1
                url = url_base.replace(url_book, row[1]).replace(url_chapter, str(index))
                print("Bible: " + url_bible + ", Book: " + row[0] + ", Chapter: " + str(index))
                try:
                    response = requests.get(url)
                except:
                    go = False
                    continue
                
                if response.status_code == 200:
                    chapter = SourceGetter.process_html(response)
                    if len(chapter) > 0:
                        book = book + "Capitulo " + str(index) + "\n"
                        book = book + chapter + "\n"
                    else:
                        go = False
                else:
                    print("Failed to retrieve the page. Status code:", \
                        response.status_code)
                    continue
            
            filename = directory + "/" + row[0] + ".txt"
            SourceGetter.write(book, filename)
        print('Done.')
        
SourceGetter = SourceGetter()
SourceGetter.make_directory(directory)
SourceGetter.pull_html_data()