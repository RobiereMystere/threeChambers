import itertools
from time import perf_counter

from loglib import log

from database_utils import DatabaseUtils

alphabet = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
    "K": 20,
    "L": 30,
    "M": 40,
    "N": 50,
    "O": 60,
    "P": 70,
    "Q": 80,
    "R": 90,
    "S": 100,
    "T": 200,
    "U": 300,
    "V": 400,
    "W": 500,
    "X": 600,
    "Y": 700,
    "Z": 800
}


def gen_combination_values(n):
    comb_values = {}
    for i in range(n + 1):
        for product in itertools.product(alphabet.keys(), repeat=i):
            prod = list(product)
            prod.sort()
            value = 0
            comb = ""
            for char in prod:
                value += alphabet[char]
                comb += char
            try:
                comb_values[value].add(comb)
            except KeyError:
                comb_values[value] = set()
                comb_values[value].add(comb)
    return comb_values


def gematria(word):
    result = 0
    for char in word:
        result += alphabet[char]
    return result


values = gen_combination_values(2)


def splitter(string):
    for i in range(1, len(string)):
        start = string[0:i]
        end = string[i:]
        yield start, end
        for split in splitter(end):
            result = [start]
            result.extend(split)
            yield result


def combinations_w(word):
    """returns all possible word with replacement by each letter value """
    letters_values = []
    for c in word:
        try:
            letters_values.append(alphabet[c])
        except KeyError:
            alphabet[c] = gematria(c)
            letters_values.append(alphabet[c])
    word_poss = []
    for l_value in letters_values:
        try:
            word_poss.append(list(values[l_value]))
        except KeyError:
            return None
    poss = []
    for i in set(itertools.product(*word_poss)):
        poss.append("".join(i))
    return poss


def chronomeister(function, *args):
    start = perf_counter()
    function(*args)
    stop = perf_counter()
    return stop - start


def permute(word):
    founds = []
    permutations = set(itertools.permutations(word))
    count = 0
    for permutation1 in permutations:
        permutation = "".join(permutation1)
        print("processing " + permutation, f"({100 * count / len(permutations)} %)")
        combinations = list(splitter(permutation))
        for combi in combinations:
            combs = combinations_w(combi)
            if combs is not None:
                combs = set(combs)
                for combination_w in combs:
                    start = perf_counter()
                    for perm_c in set(itertools.permutations(combination_w)):
                        permutation_c = "".join(perm_c)
                        if permutation_c.upper() in english \
                                and permutation_c not in founds \
                                and perm_c not in permutations:
                            founds.append(permutation_c)
                            print("\tFOUND " + permutation_c)
                    stop = perf_counter()
                    print(f"{combination_w}\t{stop - start}")
        count += 1
    print("Done 100 % :D !")
    return founds


if __name__ == '__main__':
    dbu = DatabaseUtils("database/words.db")
    select = dbu.select("words", "english")
    english = []
    for element in select:
        english.append(element[0])
    dbu.close()
    n_gram = 2
    values = gen_combination_values(n_gram)
    word1 = "ZION"
    start = perf_counter()
    founds = permute(word1)
    stop = perf_counter()
    print(founds)
