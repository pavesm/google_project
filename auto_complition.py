from collections import defaultdict
from auto_complete_data import AutoCompleteData


subs = defaultdict(set)
all_sentences = [("hello big and wonderful world", "p.css"), ("hello world", "hello.html")]


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


def getScore(sub_string, completed_sentence):
    if sub_string in completed_sentence:
        return len(sub_string) * 2


def get_best_k_completions(sub_string):
    indexes = get_common_sentences(subs[sub_string])
    AutoCompleteDataList = []
    for index in indexes:
        completed_sentence = all_sentences[index][0]
        source_text = all_sentences[index][1]
        offset = all_sentences[index][0].index(sub_string)
        score = getScore(sub_string, completed_sentence)
        AutoCompleteDataList.append(AutoCompleteData(completed_sentence, source_text, offset, score))

    return AutoCompleteDataList


def get_common_sentences(sentencesIndexes):
    if len(sentencesIndexes) <= 5:
        return list(sentencesIndexes)

    return list(sentencesIndexes)[:5]


for sentence in all_sentences:
    insert_to_dict(sentence)

get_best_k_completions(input("The system is ready. Enter your text:"))
