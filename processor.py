# By Jonathan Christen
# 2024-10-30
# My company
# My legal statement
# comment symbols (do not execute this code)
# process raw text files into LangQ readable text

import os
import re
from unicodedata import digit
import collections

def __main__():
     ### Pulls Bible chapters and processes them into a book. ###
    processor = processor()


    processor.paths(directory)
    output = ""

    for key, filename in filenames.items():
        print(key,filename)
        data = processor.read_chapter(directory + filename)
        data = processor.process_data(data)
        output += "Capítulo " + filename.split("-")[-1].split(".")[0] + '\n'
        output += data + '\n'
    processor.write(output, directory, book)
    return 0

class processor:
    ### facilitates and processes chapters into a final book ###
    def __init__(self):
        ### constructor ###
        return 0

    def path(self, directory):
        self._directory = "libre-de-salmo-1//"
        self._book = self._directory[:-2].replace("-", " ").title() + '.txt'
        self._filenames = self.__get_filenames(self._directory, self._book)
        return 0

    def __get_filenames(self):
        filenames = next(os.walk(self._directory), (None, None, []))[2]  # [] if no file
        if len(filenames) == 0:
            print('No chapter files found.')

        filename_dict = {}
        for filename in filenames:
            if not filename.endswith(".txt") and filename.split(".")[0] != self._directory[:-2]:
                continue
            if filename == (book):
                continue
            filename_dict[int(filename.split("-")[-1].split(".")[0])] = filename
        filename_dict = collections.OrderedDict(sorted(filename_dict.items()))
        return filename_dict


    def write(self, output):
        ### Write chapter  ###
        filename = self._directory + self._book
        f = open(filename, "w", encoding='utf-8')
        f.write(output)
        f.close()
        return 0

    def process_data(self, data):
        processed_data = ""
        for line in data:
            if line[0].isdigit():
                for index,char in enumerate(line):
                    if not char.isdigit():
                        if char != " ":
                            processed_data += line[:index] + " " + line[index:]
                            break
                        else:
                            processed_data += line
                            break
            else:
                processed_data += line
        # Edge cases
        processed_data.replace(u"00B6", "")
        return processed_data


    def read_chapter(self, path):
        f = open(path, "r", encoding='utf-8')
        data = f.readlines()
        f.close()
        return data

if __name__ == '__main__':
    __main__()
