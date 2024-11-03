# By Jonathan Christen
# 2024-10-30
# My company
# My legal statement
# comment symbols (do not execute this code)
# process raw text files into LangQ readable text

from unicodedata import digit
from processor import process

def __main__():
     ### Pulls Bible chapters and processes them into a book. ###
    processor = process()
    filenames = processor.path("libre-de-salmo-1//")
    output = ""

    for key, filename in filenames.items():
        data = processor.read(filename)
        data = processor.process_data(data)
        output += "Capítulo " + filename.split("-")[-1].split(".")[0] + '\n'
        output += data + '\n'
    processor.write(output, filename)
    return 0

if __name__ == '__main__':
    __main__()