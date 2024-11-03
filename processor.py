# By Jonathan Christen
# 2024-11-2
# My company
# My legal statement
# comment symbols (do not execute this code)
# process raw text files into LangQ readable text

import os
from unicodedata import digit
import collections

class process:
    ### facilitates and processes chapters into a final book ###
    def __init__(self):
        ### constructor ###
        return None
    
    def __del__(self):
        ### deconstructor ###
        return 0

    def path(self, directory):
        ### Gets book name from a directory and returns .txt file names in that directory. ###
        self._directory = directory
        self._book = self._directory[:-2].replace("-", " ").title() + '.txt'
        return self.__get_filenames()

    def __get_filenames(self):
        filenames = next(os.walk(self._directory), (None, None, []))[2]  # [] if no file
        if len(filenames) == 0:
            print('No chapter files found.')

        filename_dict = {}
        for filename in filenames:
            if not filename.endswith(".txt") and filename.split(".")[0] != self._directory[:-2]:
                continue
            if filename == (self._book):
                continue
            filename_dict[int(filename.split("-")[-1].split(".")[0])] = filename
        filename_dict = collections.OrderedDict(sorted(filename_dict.items()))
        return filename_dict


    def write(self, output, filename):
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


    def read(self, filename):
        path = self._directory + filename
        f = open(path, "r", encoding='utf-8')
        data = f.readlines()
        f.close()
        return data