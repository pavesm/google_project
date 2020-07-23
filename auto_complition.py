from collections import defaultdict, OrderedDict
from auto_complete_data import AutoCompleteData
from read_from_files import all_sentences
import string


subs = defaultdict(set)


def valid_string(string):
    string = string.lower()
    i = 0
    while i < len(string):
        if not(string[i].isalpha() or string[i].isdigit()):
            if string[i] == " ":
                i += 1
                while i + 1 < len(string) and string[i] == string[i + 1]:
                    string = string[i + 1].replace(string[i], "", 1)

            else:
                string = string.replace(string[i], "", 1)

        i += 1
    return string.lower()


def insert_to_dict():
    for i in range(len(all_sentences)):
        sentence = all_sentences[i].completed_sentence
        sentence = valid_string(sentence)
        for j in range(len(sentence)):
            subs[sentence[:j + 1]].add(i)
            subs[sentence[j:]].add(i)

        length = len(sentence)

        for k in range(length):
            for j in range(length):
                if j > length - k:
                   break

                subs[sentence[j:length - k]].add(i)


def get_score(sub_string):
    score = defaultdict(set)
    basic_score = len(sub_string) * 2
    indexes = subs[sub_string]
    if indexes:
        score[basic_score] = indexes
        if len(indexes) >= 5:
            return score

    for i in range(len(sub_string)):
        indexes = subs.get(sub_string.replace(sub_string[i], "", 1))
        if indexes:
            if i < 4:
               score[basic_score - (10 - i * 2)] = indexes

            else:
                score[basic_score - 2] = indexes

    all_alphabet = string.ascii_lowercase
    for i in range(len(sub_string)):
        for letter in all_alphabet:
            indexes = subs.get(sub_string[:i] + letter + sub_string[i:])
            if indexes:
                if i < 4:
                    score[basic_score - (10 - i * 2)] = indexes

                else:
                    score[basic_score - 2] = indexes

    for i in range(len(sub_string)):
        for letter in all_alphabet:
            indexes = subs.get(sub_string.replace(sub_string[i], letter, 1))
            if indexes:
                if i < 5:
                    score[basic_score - (5 - i)] = indexes

                else:
                    score[basic_score - 1] = indexes

    return score


def get_best_k_completions(sub_string):
    indexes = get_common_sentences(get_score(sub_string))
    auto_complete_data = []
    for i in indexes:
        auto_complete_data.append(all_sentences[i])

    return auto_complete_data


def get_common_sentences(score):
    sorted_dict = OrderedDict(sorted(score.items(), reverse=True))
    five_common_sentences = []

    for key in sorted_dict.keys():
        while sorted_dict[key] and len(five_common_sentences) < 5:
            index = sorted_dict[key].pop()
            if index not in five_common_sentences:
                all_sentences[index].score = key
                five_common_sentences.append(index)

    return five_common_sentences


def five_auto_complete_data():
    string = input("The system is ready. Enter your text:")
    string = valid_string(string)
    auto_complete_data = get_best_k_completions(string)
    if auto_complete_data:
        for item in auto_complete_data:
            print(item.completed_sentence)


insert_to_dict()

for i in range(20):
    five_auto_complete_data()
