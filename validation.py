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


def validate(set_of_doc_numbers):
    """Check quality of the solution.
    
    This function takes a set of numbers of documents as input, computes several quality metrics of the solution
    and returns a namedtuple with them.
    Computed metrics are
    1. precision
    2. recall
    3. F1-measure
    """
    true_positives = 0
    precision_denominator = 0
    recall_denominator = 0

    for i in set_of_doc_numbers:
        solution_file_path = "solutions/solution" + str(i) + ".txt"
        answer_file_path = "train/art" + str(i) + ".opin.txt"
        if os.path.isfile(solution_file_path) and os.path.isfile(answer_file_path):
            solution_file = open(solution_file_path, "r")
            answer_file = open(answer_file_path, "r")
            our_answers = read_file(solution_file)
            correct_answers = read_file(answer_file)
            true_positives += len(our_answers & correct_answers)
            precision_denominator += len(our_answers)
            recall_denominator += len(correct_answers)

    estimation = namedtuple("estimation", ["precision", "recall", "f1_measure"])
    precision = true_positives / precision_denominator
    recall = true_positives / recall_denominator
    f1_measure = 2 / (1 / precision + 1 / recall)
    return estimation(precision, recall, f1_measure)


s = set()
s.add(1)
print(validate(s))
