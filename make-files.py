import os

def __main__():
    reletive_directory = "libre-de-salmo-1//salmo-"
    for i in range(1,42):
        path = reletive_directory + str(i) + ".txt"
        f = open(path, "w")
        f.close()
if __name__ == __main__():
    __main__()