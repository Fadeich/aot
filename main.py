import os
import re
from pymystem3 import Mystem
import validation

# ToDo: (important) check if a word is an entity and correct it's register and for other make lowercase
# ToDo: there are operators of len >= 2, but the cannot be found in list of words (sentence)
def read_operators_file():  # tested
    """Returns a dictionary, key is word, and value is value"""
    operators = {}
    operators_file = open("operators.txt", "r")
    for line in operators_file:
        operators[line.rsplit(None, 1)[0].lower()] = int(line.rsplit(None, 1)[1])
    return operators


def read_sentiment_file():  # tested
    sentimental_words = {}
    sentiment_file = open("RuSentiLex2017_revised_2.txt", "r")
    for line in sentiment_file:
        if len(line) > 0 and line[0] != "!":
            sentimental_words[re.split("\W+", line)[0]] = re.split("\W+", line)[3]
    sentiment_file.close()
    return sentimental_words


def read_input_file(file_number, lemmatizer):  # tested
    sentences = []
    file_name = "test/art" + str(file_number) + ".txt"
    file = open(file_name, "r")
    for line in file:
        line = line.split(None, 2)
        if len(line) > 2:
            line = line[2].strip()
            sentence = lemmatize_with_case_saving(lemmatizer, line)
            sentence = " ".join(sentence)
            sentences.append(sentence)
    file.close()
    return sentences


def lemmatize_with_case_saving(lemmatizer, line):
    sentence = lemmatizer.lemmatize(line)
    sentence = "".join(sentence)
    line = re.split("\W+", line)
    sentence = re.split("\W+", sentence)
    line = list(filter(lambda a: a, line))
    sentence = list(filter(lambda a: a, sentence))

    for i in range(len(line)):
        if line[i].isupper():
            sentence[i] = sentence[i].upper()
        elif line[i][0].isupper():
            sentence[i] = sentence[i].capitalize()
    return sentence


def is_latin(word):  # tested
    return (word[0] >= "a" and word[0] <= "z") or (word[0] >= 'A' and word[0] <= 'Z')


def read_file_with_entities(file_number, lemmatizer):  # tested
    """Returns set of entities"""
    file_name = "test/art" + str(file_number) + ".ann"
    file = open(file_name, "r")
    set_of_entities = set()
    for line in file:
        line = line.split(None, 4)
        if len(line) < 5:
            continue
        word = line[4]
        if not is_latin(word):
            set_of_entities.add(" ".join(lemmatize_with_case_saving(lemmatizer, word)))
    file.close()
    return set_of_entities


def find_entities(sentence, entities):  # tested
    entities_in_sentence = set()
    for entity in entities:
        if entity in sentence:
            entities_in_sentence.add(entity)
    return entities_in_sentence


def calculate_sentiment(sentence, sentimental_words, operators, set_of_entities):  # tested
    list_of_words = sentence.split()
    for i in range(len(list_of_words)):
        if list_of_words[i] in sentimental_words:
            if sentimental_words[list_of_words[i]] == "positive":
                list_of_words[i] = [list_of_words[i], 1]
            elif sentimental_words[list_of_words[i]] == "negative":
                list_of_words[i] = [list_of_words[i], -1]
            else:
                list_of_words[i] = [list_of_words[i], 0]
        else:
            list_of_words[i] = [list_of_words[i], 0]
    for i in range(len(list_of_words)):
        if list_of_words[i][0] in operators:
            for j in range(i + 1, len(list_of_words)):
                if list_of_words[j][1] == 0:
                    break
                else:
                    list_of_words[j][1] *= operators[list_of_words[i][0]]

    sentiment = 0
    for word in list_of_words:
        sentiment += word[1]
    if sentiment < 0:
        return "neg"
    elif sentiment > 0:
        return "pos"
    else:
        return ""


def find_pairs_of_related_entities(sentence, sentiment, set_of_entities):  # tested
    """Return set of triples (entity, entity, sentiment)

    Just takes as a subject the first entity in sentence and as object the last entity in sentence
    """
    resulting_set = set()
    list_of_entities = list(set_of_entities)
    subject_entity = ""
    object_entity = ""
    for entity1 in list_of_entities:
        for entity2 in list_of_entities:
            if adjusted_additional_requirements(entity1, entity2):
                subject_entity = entity1
                object_entity = entity2
                resulting_set.add(tuple([subject_entity, object_entity, sentiment]))
    return resulting_set


def adjusted_additional_requirements(entity1, entity2):
    if entity1 in entity2 or entity2 in entity1:
        return False
    if len(entity1) >= 25 or len(entity2) >= 25:
        return False
    return True


def write_in_resulting_file(file_num, set_of_relations):  # tested
    file_name = "test/art" + str(file_num) + ".opin.txt"
    file = open(file_name, "w")
    for record in set_of_relations:
        file.write(record[0] + ", " + record[1] + ", " + record[2] + "\n")
    file.close()


def main():
    lemmatizer = Mystem()
    operators = read_operators_file()
    sentimental_words = read_sentiment_file()
    set_of_relations = set()  # set of triples (entity, entity, sentiment)
    dir_name = "test/"
    for d, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".ann"):  # Just to choose one of three files with equal number and take it's number
                if file[4].isdigit():
                    file_num = int(file[3:5])
                else:
                    file_num = int(file[3])
                sentences = read_input_file(file_num, lemmatizer)
                entities = read_file_with_entities(file_num, lemmatizer)
                for sentence in sentences:
                    entities_in_sentence = find_entities(sentence, entities)
                    if len(entities_in_sentence) > 1:
                        sentiment = calculate_sentiment(sentence,
                                                        sentimental_words,
                                                        operators,
                                                        entities_in_sentence)
                        if sentiment != "":
                            set_of_relations |= find_pairs_of_related_entities(sentence,
                                                                               sentiment,
                                                                               entities_in_sentence)
                write_in_resulting_file(file_num, set_of_relations)
                set_of_relations = set()


main()
print(validation.validate())

# Можно брать местоимения в тексте и заменять их на сущности, разберись ещё, в каких случаях надо разрешать
# анафору
# разберись с подходами на правила и на машинке (и где обучаться в таком случае)

# найти для каждого местоимения антицидент (идём по тексту, находим кандидутов,
# фильтруем тех, которые не согласуюnся по роду и числу)
# ранжирование гипотех
# признаки: расстояние между анафором и антицидентом (больше 90% антицидентов в том же и предыдущем предложении)
# если есть слово "которая", перед ним запятиая, а перед запятой именная группа
# Чем длиннее именная группа в словах, тем более вероятно встретить анафору дальше
# (длиннее имеется ввиду в символах)
