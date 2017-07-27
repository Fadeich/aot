import os


def read_syntaxnet(file_number):
    """Read a syntaxnet output file for one document and return list of sentences"""
    # fr = pd.read_csv("syntaxnet_output_with_tone.csv", sep="\t", encoding="utf-8")
    tokens = []
    filename = "syntaxnet_output" + str(file_number)
    file = open(filename, "r")
    for line in file:
        line = line.strip()
        token = line.split("\t")[1:]
        tokens.append(token)
    sentences = []
    cur_sentence = []
    cur_sentence_id = 1
    for token in tokens:
        if token[6] != cur_sentence_id:
            sentences.append(cur_sentence)
            cur_sentence = []
            cur_sentence_id = token[6]
        cur_sentence.append(token)

    return sentences


def find_entities(sentence):
    lemmatized_form = 5
    entities_in_sentence = set()
    for word in sentence:
        if is_entity(word):
            entities_in_sentence.add(word[lemmatized_form])
    return entities_in_sentence


def calculate_sentiment(sentence):
    operators = read_operators_file()
    for i in range(len(sentence)):
        if sentence[i] in operators:
            for j in range(i + 1, len(sentence)):
                if sentence[j][7] == 0:
                    break
                else:
                    sentence[j][7] *= operators[sentence[i]]
            for j in reversed(range(i - 1)):
                if sentence[j][7] == 0:
                    break
                else:
                    sentence[j][7] *= operators[sentence[i]]
    sentiment = 0
    for word in sentence:
        sentiment += word[7]

    if sentiment < 0:
        return "neg"
    elif sentiment == 0:
        return ""
    else:
        return "pos"


def read_operators_file():
    operators = {}
    operators_file = open("operators.txt", "r")
    for line in operators_file:
        operators[line.split()[0].lower()] = int(line.split()[1])
    return operators


def is_entity(word):
    if word[8] != "":
        return True
    else:
        return False


def is_sentimental(word):
    if word[7] != 0:
        return True
    else:
        return False


def find_pairs_of_related_entities(sentence, sentiment):
    """Return set of triples (entity, entity, sentiment)

    Just takes as a subject the first entity in sentence and as object the last entity in sentence
    """
    lemmatized_form = 5
    subject_entity = ""
    object_entity = ""
    for word in sentence:
        if is_entity(word):
            subject_entity = word[lemmatized_form]
    for word in reversed(sentence):
        if is_entity(word):
            object_entity = word[lemmatized_form]
    return tuple(subject_entity, object_entity, sentiment)


def write_in_resulting_file(file_num, set_of_relations):
    file_name = "test/art" + str(file_num) + ".opin.txt"
    file = open(file_name, "w")
    for record in set_of_relations:
        file.write(record[0] + ", " + record[1] + ", " + record[3] + "\n")


def main():
    set_of_relations = set()  # set of triples (entity, entity, sentiment)
    dir_name = "test/"
    for d, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith(".ann"):  # Just to choose one of three files with equal number and take it's number
                if file[4].isdigit():
                    file_num = int(file[3:5])
                else:
                    file_num = int(file[3])
                sentences = read_syntaxnet(file_num)
                for sentence in sentences:
                    entity_set = find_entities(sentence)
                    if len(entity_set) > 1:
                        sentiment = calculate_sentiment(sentence)
                        if sentiment != "":
                            set_of_relations.add(find_pairs_of_related_entities(sentence, sentiment))
                write_in_resulting_file(file_num, set_of_relations)


main()

# Можно брать местоимения в тексте и заменять их на сущности, разберись ещё, в каких случаях надо разрешать
# анафору
# разберись с подходами на правила и на машинке (и где обучаться в таком случае)

# найти для каждого местоимения антицидент (идём по тексту, находим кандидутов, фильтруем тех, которые не согласующихся по роду и числу)
# ранжирование гипотех
# признаки: расстояние между анафором и антицидентом (больше 90% антицидентов в том же и предыдущем предложении)
# если есть слово "которая", перед ним запятиая, а перед запятой именная группа
# Чем длиннее именная группа в словах, тем более вероятно встретить анафору дальше (длиннее имеется ввиду в символах)
