import itertools

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
            value = 0
            comb = ""
            for char in product:
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


def combinations_w(word):
    """returns all possible word with replacement by each letter value """
    letters_values = []
    for c in word:
        letters_values.append(alphabet[c])
    word_poss = []
    for l_value in letters_values:
        word_poss.append(list(values[l_value]))
    poss = []
    for i in set(itertools.product(*word_poss)):
        poss.append("".join(i))
    return poss


if __name__ == '__main__':
    dbu = DatabaseUtils("database/words.db")
    values = gen_combination_values(2)
    for i in combinations_w("ZION"):
        indb = dbu.select_one("words", "english", "english = '" + i.upper() + "'")
        if indb is not None:
            print(indb[0])
    dbu.close()
