from collections import defaultdict, OrderedDict
from auto_complete_data import AutoCompleteData
from read_from_files import all_sentences
import string


subs = defaultdict(set)


def insert_to_dict():
    for j in range(len(all_sentences)):
        sentence = all_sentences[j].completed_sentence
        for i in range(len(sentence)):
            subs[sentence[:i + 1]].add(j)
            subs[sentence[i:]].add(j)

        length = len(sentence)

        for i in range(length):
            for k in range(length):
                if k > length - i:
                   break

                subs[sentence[k:length - i]].add(j)


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
    score = get_score(sub_string)
    indexes = get_common_sentences(score)
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


insert_to_dict()

five_common_sentencens = get_best_k_completions(input("The system is ready. Enter your text:"))
for item in five_common_sentencens:
    print(item.completed_sentence)