from collections import defaultdict
from auto_complete_data import AutoCompleteData
# from read_from_files import all_sentences
import string

subs = defaultdict(set)
all_sentences = [("hello big and nice world", "hi.css"), ("hello world", "h.html")]


def insert_to_dict(sentence):
    for i in range(len(sentence)):
        subs[sentence[:i + 1]].add(all_sentences.index(sentence))
        subs[sentence[i:]].add(all_sentences.index(sentence))

    length = len(sentence)

    for i in range(length):
        for j in range(length):
            if j > length - i:
               break

            subs[sentence[j:length - i]].add(all_sentences.index(sentence))


def get_score(sub_string):
    score = defaultdict(set)
    basic_score = len(sub_string) * 2
    indexes = subs.get(sub_string)
    if indexes:
        score[basic_score] = indexes
        if indexes >= 5:
            return score

    for i in range(len(sub_string)):
        indexes = subs.get(sub_string.replace(sub_string[i], ""))
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
            indexes = subs.get(sub_string.replace(sub_string[i], letter))
            if indexes:
                if i < 5:
                    score[basic_score - (5 - i)] = indexes

                else:
                    score[basic_score - 1] = indexes

    return score


def get_best_k_completions(sub_string):
    score = get_score(sub_string)
    indexes = get_common_sentences(score)
    auto_complete_data_list = []
    for index in indexes:
        completed_sentence = all_sentences[index][0]
        source_text = all_sentences[index][1]
        offset = all_sentences[index][0].index(sub_string)
        auto_complete_data_list.append(AutoCompleteData(completed_sentence, source_text, offset, score))

    return auto_complete_data_list


def get_common_sentences(score):
    


for sentence in all_sentences:
    insert_to_dict(sentence)

get_best_k_completions(input("The system is ready. Enter your text:"))
