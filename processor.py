# By Jonathan Christen

import requests
from bs4 import BeautifulSoup
import os   
from inputs import *
import time
import string

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
        processed_string = None
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

                # First use.
                if processed_string == None:
                    processed_string = verse
                    continue

                # Edge cases.
                if  verse == 'eñor':
                    processed_string = processed_string + verse
                    continue
                
                if  processed_string[-1] in [ ' ' ] or\
                    verse[0]             in [ ' ' ] or\
                    processed_string[-1].isalpha() and verse[0] in \
                        [ ':', ',', '.', '?', '!' ]:
                    processed_string = processed_string + verse
                    continue
                
                if processed_string[-1].isalpha() and verse[0] in [':',',','.']:
                    processed_string = processed_string + verse
                    continue
                    

                processed_string = processed_string + " "  + verse
        
        # No chapter case.
        if processed_string == None:
            return str()
        
        return processed_string.split("</path></svg>")[-1]
        
    def pull_html_data(self):
        ''' '''
        print( 'Comenzar | Biblia   | ' + url_bible )
        for row in table:
            print("Comenzar | Libre    | " + row[0] )
            book = ""
            go  = True
            index = int(0)
            while go == True:
                index += 1
                url = url_base.replace( url_book, row[1] )\
                    .replace( url_chapter, str(index) )
                
                try:
                    # Sometimes pulling information to quickly trigers errors 
                    # in the web server.
                    time.sleep(0.5)
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
                print("Completo | Capitulo | " + str(index))
            filename = directory + "/" + row[0] + ".txt"
            SourceGetter.write(book, filename)
        print('Done.')
        
SourceGetter = SourceGetter()
SourceGetter.make_directory(directory)
SourceGetter.pull_html_data()