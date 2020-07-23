from collections import defaultdict, OrderedDict
from read_from_files import all_sentences
import string


subs = defaultdict(set)


def valid_string(string):
    i = 0

    while i < len(string):
        if not (string[i].isalpha() or string[i].isdigit()):
            if string[i] == ' ':
                i += 1
                while i < len(string) and string[i] == ' ':
                    string = string.replace(string[i], "", 1)

            else:
                string = string.replace(string[i], "", 1)

        i += 1

    return string.lower()


def insert_to_dict():
    for i in range(len(all_sentences)):
        sentence = all_sentences[i].completed_sentence
        sentence = valid_string(sentence)
        for j in range(len(sentence)):
            if sentence[j] != " ":
                subs[sentence[:j + 1]].add(i)
                subs[sentence[j:]].add(i)

        length = len(sentence)

        for k in range(length):
            for j in range(length):
                if j > length - k:
                   break

                if sentence[j] != " " and sentence[length - k - 1] != " ":
                    subs[sentence[j:length - k]].add(i)


def delete_letter(score, basic_score, sub_string):
    for i in range(len(sub_string)):
        indexes = subs.get(sub_string.replace(sub_string[i], "", 1))
        if indexes:
            if i < 4:
               score[basic_score - (10 - i * 2)] = indexes

            else:
                score[basic_score - 2] = indexes

    return score


def add_letter(score, basic_score, sub_string):
    all_alphabet = string.ascii_lowercase
    for i in range(len(sub_string)):
        for letter in all_alphabet:
            indexes = subs.get(sub_string[:i] + letter + sub_string[i:])
            if indexes:
                if i < 4:
                    score[basic_score - (10 - i * 2)] = indexes

                else:
                    score[basic_score - 2] = indexes

    return score


def replace_letter(score, basic_score, sub_string):
    all_alphabet = string.ascii_lowercase
    for i in range(len(sub_string)):
        for letter in all_alphabet:
            indexes = subs.get(sub_string.replace(sub_string[i], letter, 1))
            if indexes:
                if i < 5:
                    score[basic_score - (5 - i)] = indexes

                else:
                    score[basic_score - 1] = indexes

    return score


def get_score(sub_string):
    score = defaultdict(set)
    basic_score = len(sub_string) * 2
    indexes = subs[sub_string]
    if indexes:
        score[basic_score] = indexes
        if len(indexes) >= 5:
            return score

    score = delete_letter(score, basic_score, sub_string)

    score = add_letter(score, basic_score, sub_string)

    score = replace_letter(score, basic_score, sub_string)

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
    while True:
        my_string = input("Enter your text:")
        string = ""

        while True:
            my_string += string
            auto_complete_data = get_best_k_completions(valid_string(my_string))

            if auto_complete_data:
                print(f"Here are {len(auto_complete_data)} suggestions")
                for i in range(len(auto_complete_data)):
                    print(f"{i+1}. {auto_complete_data[i].completed_sentence}, ({auto_complete_data[i].source_text})")

            string = input(my_string)
            if string == '#':
                break

        if string == "stop":
            break


insert_to_dict()

five_auto_complete_data()
