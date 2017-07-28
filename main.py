import os
import re
from pymystem3 import Mystem


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
    print(sentimental_words)
    return sentimental_words


def read_input_file(file_number, lemmatizer):  # tested
    sentences = []
    file_name = "test/art" + str(file_number) + ".txt"
    file = open(file_name, "r")
    for line in file:
        line = line.split(None, 2)
        if len(line) > 2:
            line = line[2].strip()
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
            sentence = " ".join(sentence)
            sentences.append(sentence)
    return sentences


def is_latin(word):  # tested
    return (word[0] >= "a" and word[0] <= "z") or (word[0] >= 'A' and word[0] <= 'Z')


def read_file_with_entities(file_number):
    """Returns set of entities"""
    file_name = "test/art" + str(file_number) + ".txt"
    file = open(file_name, "r")
    set_of_entities = set()
    for line in file:
        set_of_entities.add(line.rsplit(None, 1)[1])
    return set_of_entities


def read_sentimental_words():
    print()

def read_syntaxnet(file_number):  # tested
    """Read a syntaxnet output file for one document and return list of sentences"""
    # fr = pd.read_csv("syntaxnet_output_with_tone.csv", sep="\t", encoding="utf-8")
    tokens = []
    file_name = "output/syntaxnet_output" + str(file_number) + ".csv"
    file = open(file_name, "r")
    for line in file:
        line = line.strip()
        token = line.split("\t")[1:]
        if token[0] != "word" and len(token) == 9:  # crutch
            tokens.append(token)
    sentences = []
    cur_sentence = []
    cur_sentence_id = "1"
    for token in tokens:
        if token[6] != cur_sentence_id:
            sentences.append(cur_sentence)
            cur_sentence = []
            cur_sentence_id = token[6]
        cur_sentence.append(token)

    return sentences


def find_entities(sentence):  # tested
    lemmatized_form = 5
    entities_in_sentence = set()
    for word in sentence:
        if is_entity(word):
            entities_in_sentence.add(word[lemmatized_form])
    return entities_in_sentence


def is_entity(word):  # tested
    if word[8] != "0" and not is_latin(word[1].lower()):
        return True
    else:
        return False


def calculate_sentiment(sentence, operators):  # tested
    lemmatized_form = 5
    sentiment_label = 7
    for i in range(len(sentence)):
        if sentence[i][lemmatized_form] in operators:
            for j in range(i + 1, len(sentence)):
                if sentence[j][sentiment_label] == "0":
                    break
                else:
                    new_value = int(sentence[j][sentiment_label]) * operators[sentence[i][lemmatized_form]]
                    sentence[j][sentiment_label] = str(int(new_value))
            for j in reversed(range(i - 1)):
                if sentence[j][sentiment_label] == "0":
                    break
                else:
                    new_value = int(sentence[j][sentiment_label]) * operators[sentence[i][lemmatized_form]]
                    sentence[j][sentiment_label] = str(int(new_value))

    sentiment = 0
    for word in sentence:
        sentiment += int(word[sentiment_label])
    if sentiment < 0:
        return "neg"
    elif sentiment > 0:
        return "pos"
    else:
        return ""


def find_pairs_of_related_entities(sentence, sentiment):  # tested
    """Return set of triples (entity, entity, sentiment)

    Just takes as a subject the first entity in sentence and as object the last entity in sentence
    """
    lemmatized_form = 5
    subject_entity = ""
    object_entity = ""
    resulting_set = set()
    for word in sentence:
        if is_entity(word):
            subject_entity = word[lemmatized_form]
            break
    for word in reversed(sentence):
        if is_entity(word):
            object_entity = word[lemmatized_form]
            break
    resulting_set.add(tuple([subject_entity, object_entity, sentiment]))
    return resulting_set


def write_in_resulting_file(file_num, set_of_relations):  # tested
    file_name = "test/art" + str(file_num) + ".opin.txt"
    file = open(file_name, "w")
    for record in set_of_relations:
        file.write(record[0] + ", " + record[1] + ", " + record[2] + "\n")


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
                for sentence in sentences:
                    entity_set = find_entities(sentence)
                    if len(entity_set) > 1:
                        sentiment = calculate_sentiment(sentence, operators)
                        if sentiment != "":
                            set_of_relations |= find_pairs_of_related_entities(sentence, sentiment)
                write_in_resulting_file(file_num, set_of_relations)
                set_of_relations = set()


main()

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
