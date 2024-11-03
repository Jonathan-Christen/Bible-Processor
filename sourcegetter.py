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


table = [
        ["Génesis",      "https://www.bible.com/es/bible/103/GEN.1.NBLA"],
        ["Éxodo",        "https://www.bible.com/es/bible/103/EXO.1.NBLA"],
        ["Levítico",     "https://www.bible.com/es/bible/103/LEV.1.NBLA"],
        ["Números",      "https://www.bible.com/es/bible/103/NUM.1.NBLA"],
        ["Deuteronomio", "https://www.bible.com/es/bible/103/DEU.1.NBLA"],
        ["Josué",        "https://www.bible.com/es/bible/103/JOS.1.NBLA"],
        ["Jueces",       "https://www.bible.com/es/bible/103/JDG.1.NBLA"],
        ["Rut",          "https://www.bible.com/es/bible/103/RUT.1.NBLA"],
        ["Samuel 1",     "https://www.bible.com/es/bible/103/1SA.1.NBLA"],
        ["Samuel 2",     "https://www.bible.com/es/bible/103/2SA.1.NBLA"],
        ["Reyes 1",      "https://www.bible.com/es/bible/103/1KI.1.NBLA"],
        ["Reyes 2",      "https://www.bible.com/es/bible/103/2KI.1.NBLA"],
        ["Crónicas 1",   "https://www.bible.com/es/bible/103/1CH.1.NBLA"],
        ["Crónicas 2",   "https://www.bible.com/es/bible/103/2CH.1.NBLA"],
        ["Esdras",       "https://www.bible.com/es/bible/103/EZR.1.NBLA"],
        ["Nehemías",     "https://www.bible.com/es/bible/103/NEH.1.NBLA"],
        ["Ester",        "https://www.bible.com/es/bible/103/EST.1.NBLA"],
        ["Job",          "https://www.bible.com/es/bible/103/JOB.1.NBLA"],
        ["Salmo",        "https://www.bible.com/es/bible/103/PSA.1.NBLA"],
        ["Proverbios",   "https://www.bible.com/es/bible/103/PRO.1.NBLA"],
        ["Eclesiastés",  "https://www.bible.com/es/bible/103/ECC.1.NBLA"],
        ["Cantares",     "https://www.bible.com/es/bible/103/SNG.1.NBLA"],
        ["Isaías",       "https://www.bible.com/es/bible/103/ISA.1.NBLA"],
        ["Jeremías",     "https://www.bible.com/es/bible/103/JER.1.NBLA"],
        ["Lamentaciones","https://www.bible.com/es/bible/103/LAM.1.NBLA"],
        ["Ezequiel",     "https://www.bible.com/es/bible/103/EZK.1.NBLA"],
        ["Daniel",       "https://www.bible.com/es/bible/103/DAN.1.NBLA"],
        ["Oseas",        "https://www.bible.com/es/bible/103/HOS.1.NBLA"],
        ["Joel",         "https://www.bible.com/es/bible/103/JOL.1.NBLA"],
        ["Amós",         "https://www.bible.com/es/bible/103/AMO.1.NBLA"],
        ["Abdías",       "https://www.bible.com/es/bible/103/OBA.1.NBLA"],
        ["Jonás",        "https://www.bible.com/es/bible/103/JON.1.NBLA"],
        ["Miqueas",      "https://www.bible.com/es/bible/103/MIC.1.NBLA"],
        ["Nahúm",        "https://www.bible.com/es/bible/103/NAM.1.NBLA"],
        ["Habacuc",      "https://www.bible.com/es/bible/103/HAB.1.NBLA"],
        ["Sofonías",     "https://www.bible.com/es/bible/103/ZEP.1.NBLA"],
        ["Hageo",        "https://www.bible.com/es/bible/103/HAG.1.NBLA"],
        ["Zacarías",     "https://www.bible.com/es/bible/103/ZEC.1.NBLA"],
        ["Malaquías",    "https://www.bible.com/es/bible/103/MAL.1.NBLA"],
        ["Mateo",        "https://www.bible.com/es/bible/103/MAT.1.NBLA"],
        ["Marcos",       "https://www.bible.com/es/bible/103/MRK.1.NBLA"],
        ["Lucas",        "https://www.bible.com/es/bible/103/LUK.1.NBLA"],
        ["Juan",         "https://www.bible.com/es/bible/103/JHN.1.NBLA"],
        ["Hechos",       "https://www.bible.com/es/bible/103/ACT.1.NBLA"],
        ["Romanos",      "https://www.bible.com/es/bible/103/ROM.1.NBLA"],
        ["Corintios 1",  "https://www.bible.com/es/bible/103/1CO.1.NBLA"],
        ["Corintios 2",  "https://www.bible.com/es/bible/103/2CO.1.NBLA"],
        ["Gálatas",      "https://www.bible.com/es/bible/103/GAL.1.NBLA"],
        ["Efesios",      "https://www.bible.com/es/bible/103/EPH.1.NBLA"],
        ["Filipenses",   "https://www.bible.com/es/bible/103/PHP.1.NBLA"],
        ["Colosenses",   "https://www.bible.com/es/bible/103/COL.1.NBLA"],
        ["Tesalonicenses 1",   "https://www.bible.com/es/bible/103/1TH.1.NBLA"],
        ["Tesalonicenses 2",   "https://www.bible.com/es/bible/103/2TH.1.NBLA"],
        ["Timoteo 1",    "https://www.bible.com/es/bible/103/1TI.1.NBLA"],
        ["Timoteo 2",    "https://www.bible.com/es/bible/103/2TI.1.NBLA"],
        ["Tito",         "https://www.bible.com/es/bible/103/TIT.1.NBLA"],
        ["Filemón",      "https://www.bible.com/es/bible/103/PHM.1.NBLA"],
        ["Hebreos",      "https://www.bible.com/es/bible/103/HEB.1.NBLA"],
        ["Santiago",     "https://www.bible.com/es/bible/103/JAS.1.NBLA"],
        ["Pedro 1",      "https://www.bible.com/es/bible/103/1PE.1.NBLA"],
        ["Pedro 2",      "https://www.bible.com/es/bible/103/2PE.1.NBLA"],
        ["Juan 1",       "https://www.bible.com/es/bible/103/1JN.1.NBLA"],
        ["Juan 2",       "https://www.bible.com/es/bible/103/2JN.1.NBLA"],
        ["Juan 3",       "https://www.bible.com/es/bible/103/3JN.1.NBLA"],
        ["Judas",        "https://www.bible.com/es/bible/103/JUD.1.NBLA"],
        ["Apocalipsis",  "https://www.bible.com/es/bible/103/REV.1.NBLA"]
        ]
url_end = ".NBLA"
directory = "nbla"
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