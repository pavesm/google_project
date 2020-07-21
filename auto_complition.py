from collections import defaultdict

subs = defaultdict(set)
allSentences = ["hello big and wonderful world", "hello world"]


def insertToDict(sentence):
    for i in range(len(sentence)):
        subs[sentence[:i + 1]].add(allSentences.index(sentence))
        subs[sentence[i:]].add(allSentences.index(sentence))

    length = len(sentence)

    for i in range(length):
        for j in range(length):
            if j > length - i:
               break

            subs[sentence[j:length - i]].add(allSentences.index(sentence))


def fiveAutoComplition():
    string = input("The system is ready. Enter your text:")
    indexes = getCommonSentences(subs[string])
    for index in indexes:
        print(allSentences[index])


def getCommonSentences(sentencesIndexes):
    if len(sentencesIndexes) <= 5:
        return list(sentencesIndexes)

    return list(sentencesIndexes)[:5]


for sentence in allSentences:
    insertToDict(sentence)

fiveAutoComplition()
