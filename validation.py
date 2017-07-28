import os
from collections import namedtuple


def read_file(file):
    """Parse file
    
    It takes file as input, parse into lines and entities in lines
    and returns a list of tuples (entity, entity, sentiment)
    """
    content = set()
    for line in file:
        len_of_line = 3
        list = line.split(",")[:len_of_line]
        if len(list) >= len_of_line:
            for i in range(len_of_line):
                list[i] = list[i].strip()
            if list[len_of_line - 1] == "pos" or list[len_of_line - 1] == "neg":
                content.add(tuple(list))
    return content


def validate():
    """Check quality of the solution."""
    true_positives = 0
    precision_denominator = 0
    recall_denominator = 0

    for d, dirs, files in os.walk("test/"):
        for file in files:
            if file.endswith(".opin.txt"):
                if file[4].isdigit():
                    file_num = file[3:5]
                else:
                    file_num = file[3]
                solution_file_name = "test/art" + file_num + ".opin.txt"
                answer_file_name = "train/art" + file_num + ".opin.txt"
                if not os.path.exists(solution_file_name) or not os.path.exists(answer_file_name):
                    continue
                solution_file = open(solution_file_name, "r")
                answer_file = open(answer_file_name, "r")
                our_answers = read_file(solution_file)
                correct_answers = read_file(answer_file)
                true_positives += len(our_answers & correct_answers)
                precision_denominator += len(our_answers)
                recall_denominator += len(correct_answers)

    estimation = namedtuple("estimation", ["precision", "recall", "f1_measure"])
    precision = true_positives / precision_denominator
    recall = true_positives / recall_denominator
    f1_measure = 2 / (1 / precision + 1 / recall)
    result = estimation(precision, recall, f1_measure)
    save_result(result)
    return result


def save_result(result):
    file = open("statistics_of_launches.txt", "a")
    file.write(str(result) + "\n")
    file.close()
