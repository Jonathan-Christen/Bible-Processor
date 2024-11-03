import requests
from bs4 import BeautifulSoup
import os   

class SourceGetter:
    ### Gets website data and writes it to files. ###
    
    def __init__(self):
        ### Constructor ###
        return None
    
    def __del__(self):
        ### Deconstructor ###
        return 0
    
    def write(self, data, filename):
        ### Write book ###
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
        ### processes h ###
        
        html = response.text
        html = BeautifulSoup(html, "html.parser")
        text = str(html)
        start = "R2PLt\">"
        end   = "</span>"

        verse_numbers = text.split(start)
        numbers_array = []
        for verse_number in verse_numbers:
            numbers_array.append(verse_number.split(end)[0])
        
        start = "RrUqA\">"
        end   = "</span>"
        verses = text.split(start)
        verses_string = ""
        for verse in verses:
            if len(verse) == 0:
                continue
            
            verse = verse.split(end)[0]
            if len(verses_string) > 0:
                if verses_string[-1] != " " and verse[0] != " ":
                    verses_string = verses_string + " "  + verse
                else: 
                    verses_string = verses_string + verse
            else:
                verses_string = verses_string + verse
        return verses_string.split("</path></svg>")[-1]

directory = "nbla"
table = [
        ["",    ""],
        ["Reyes 1",    "https://www.bible.com/es/bible/103/1KI.1.NBLA"],
        ["Reyes 2",    "https://www.bible.com/es/bible/103/2KI.1.NBLA"],
        ["Crónicas 1", "https://www.bible.com/es/bible/103/1CH.1.NBLA"],
        ["Crónicas 2", "https://www.bible.com/es/bible/103/2CH.1.NBLA"]
        ]
url_end = ".NBLA"
SourceGetter = SourceGetter()
SourceGetter.make_directory(directory)

for row in table:
    book = ""
    url = row[1].split(url_end)[0]
    go  = True
    index = int(0)
    while go == True:
        index += 1
        url_prepared = url[:-1] + str(index) + url_end
        print(url_prepared)
        try:
            response = requests.get(url_prepared)
        except:
            go = False
            continue
        
        if response.status_code == 200:
            chapter = SourceGetter.process_html(response)
            if len(chapter) > 0:
                book = book + "Capitulo " + str(index) + "\n"
                book = book + chapter[1:] + "\n"
            else:
                go = False
        else:
            print("Failed to retrieve the page. Status code:", response.status_code)
            continue
    
    filename = directory + "/" + row[0] + ".txt"
    SourceGetter.write(book, filename)
print('Done.')