import os
from auto_complete_data import AutoCompleteData

all_sentences = []


def read_txt_file():
    for root, dirs, files in os.walk("./my_files/python-3.8.4-docs-text/"):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), encoding="utf8") as myfile:
                    offset = 0
                    sentences = myfile.readlines()
                    for sentsnce in sentences:
                        if sentsnce:
                            offset += 1
                            all_sentences.append(AutoCompleteData(sentsnce.strip(), file, offset))


read_txt_file()
