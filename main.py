import itertools
from time import perf_counter

from loglib import Logger

from database_utils import DatabaseUtils

logger = Logger(False)

primes = [2, 3, 5, 7, 11,
          13, 17, 19, 23,
          29, 31, 37, 41,
          43, 47, 53, 59,
          61, 67, 71, 73,
          79, 83, 89, 97,
          101, 103, 107,
          109, 113, 127,
          131, 137, 139,
          149, 151, 157,
          163, 167, 173,
          179, 181, 191,
          193, 197, 199]

alphabet_three_chambers = {
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

alphabet_prime = {'A': 2,
                  'B': 3,
                  'C': 5,
                  'D': 7,
                  'E': 11,
                  'F': 13,
                  'G': 17,
                  'H': 19,
                  'I': 23,
                  'J': 29,
                  'K': 31,
                  'L': 37,
                  'M': 41,
                  'N': 43,
                  'O': 47,
                  'P': 53,
                  'Q': 59,
                  'R': 61,
                  'S': 67,
                  'T': 71,
                  'U': 73,
                  'V': 79,
                  'W': 83,
                  'X': 89,
                  'Y': 97,
                  'Z': 101
                  }

alphabet = alphabet_prime

wanted_letters = list(alphabet.keys())[:10]


def perm(word):
    permutations = set(itertools.permutations(word))
    for i in permutations:
        print(i)


def gen_combination_values(n):
    comb_values = {}
    for i in range(n + 1):
        for product in itertools.product(wanted_letters, repeat=i):
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
    logger.log(str(comb_values))
    return comb_values


def gematria(word):
    result = 0
    for char in word:
        result += alphabet[char]
    return result


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
            try:
                word_poss.append([list(alphabet.keys())[list(alphabet.values()).index(l_value)]])
            except KeyError as err:
                print("KeyError", err)
    logger.log("WORD POSSIBILITIES" + str(word_poss))
    poss = []
    for i in itertools.product(*word_poss):
        poss.append("".join(i))
    logger.log("POSSIBILITIES" + str(poss))
    return poss


def chronomeister(function, *args):
    start = perf_counter()
    function(*args)
    stop = perf_counter()
    return stop - start


def permute(word):
    founds = []

    if word not in done:
        permutations = list(set(itertools.permutations(word)))
        count = 0
        for perms in permutations:
            permutation = "".join(perms)
            print("processing " + str(permutation), f"({100 * count / len(permutations)} %)")

            combinations = list(splitter(permutation))
            for combi in combinations:
                combs = combinations_w(combi)
                if combs is not None:
                    combs = set(combs)
                    combs = list(combs)
                    for combination_w in combs:
                        if combination_w not in done:
                            permutations_comb = set(itertools.permutations(combination_w))
                            permutations_comb = list(permutations_comb)
                            start = perf_counter()
                            for perm_c in permutations_comb:
                                permutation_c = "".join(perm_c)
                                done.add(permutation_c)
                                if permutation_c.upper() in english \
                                        and permutation_c not in founds \
                                        and perm_c not in combinations:
                                    founds.append(permutation_c)
                                    print("\tFOUND " + permutation_c, gematria(permutation_c))
                            stop = perf_counter()
                            logger.log(f"{combination_w}\t{stop - start}")
            count += 1
    print("Done 100 % :D !")
    return founds


if __name__ != '__main__':
    print("{")

if __name__ == '__main__':
    start = perf_counter()
    done = set()
    dbu = DatabaseUtils("database/words.db")
    select = dbu.select("words", "english")
    english = []
    for element in select:
        english.append(element[0])
    dbu.close()
    n_gram = 2
    values = gen_combination_values(n_gram)
    word1 = "ZION"
    found_words = permute(word1)
    print(found_words)
    stop = perf_counter()
    print(f"Duration : {stop - start} secondes")
