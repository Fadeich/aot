import os


def read_file(file):
    content = set()
    for line in file:
        list = line.split(",")[:3]
        if len(list) >= 3:
            for i in range(1):
                list[i] = list[i].strip()
            if list[2] != "pos" and list[2] != "neg":
                content.add(tuple(list))
    return content


def compare(solution_file, answer_file):
    our_answers = read_file(solution_file)
    correct_answers = read_file(answer_file)
    print(correct_answers)
    # Here all the metrics will be calculated


def validate(solution_number=0):
    """Check quality of your solution.
    
    This function computes several quality metrics of your solution and returns tuple.
    You can optionally set a solution number. By default it compares and checks all the
    existing solution, which are stored in 'Solutions' directory, in this case a list of tuples will be returned.
    Computed metrics are
    1. precision on positive sample
    2. recall on positive sample
    3. F-measure on positive sample
    4. precision on negative sample
    5. recall on negative sample
    6. F-measure on negative sample
    """
    if solution_number != 0:
        solution_file_path = "solutions/solution" + str(solution_number) + ".txt"
        answer_file_path = "train/art" + str(solution_number) + ".opin.txt"
        if os.path.isfile(solution_file_path) and os.path.isfile(answer_file_path):
            solution_file = open(solution_file_path, "r")
            answer_file = open(answer_file_path, "r")
            return compare(solution_file, answer_file)
        else:
            return None
    else:
        num_of_solutions = 40
        result = []
        for i in range(num_of_solutions):
            solution_file_path = "solutions/solution" + str(i + 1) + ".txt"
            answer_file_path = "train/art" + str(i + 1) + ".opin.txt"
            if os.path.isfile(solution_file_path) and os.path.isfile(answer_file_path):
                solution_file = open(solution_file_path, "r")
                answer_file = open(answer_file_path, "r")
                result.append(compare(solution_file, answer_file))
        return result


validate(14)

