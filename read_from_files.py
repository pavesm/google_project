from os import listdir
import glob, os
from auto_complete_data import AutoCompleteData

root = "."
all_sentences = []


def read_txt_file(root):
    for root, dirs, files in os.walk("./my_files/python-3.8.4-docs-text"):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), encoding="utf8") as myfile:
                    sentences = myfile.readline()
                    for sentsnce in sentences:
                        all_sentences.append(AutoCompleteData(sentences.strip(), os.path.join(root, file),8))


read_txt_file(root)
print(all_sentences[2].completed_sentence)
