import re

from collections import Counter

def get_letters_frequency(text: str):
    text = text.upper()
    letter_counts = Counter(filter(str.isalpha, text))
    letter_frequency = {letter: count/sum(letter_counts.values()) for letter, count in letter_counts.items()}
    return letter_frequency


def get_words(text: str):
    text = text.upper()
    words = re.findall(r'\b\w+\b', text)
    return set(words)


def check(word: str, other_word: str) -> bool:
    if len(word) != len(other_word):
        return False

    letter_mapping = {}
    used_letters = set()

    for i in range(len(word)):
        letter = word[i]
        other_letter = other_word[i]

        if not letter.isalpha() or not other_letter.isalpha():
            return False

        if letter in letter_mapping:
            if letter_mapping[letter] != other_letter:
                return False
        else:
            if other_letter in used_letters:
                return False
            letter_mapping[letter] = other_letter
            used_letters.add(other_letter)

    return True



alph = 'абвгдеёжзийклмнопрстуфчцчшщъыьэюяңөү'.upper()


encoded_text = open('input.txt', 'r', encoding='UTF-8').read()
example_text = open('kyrgyz_text.txt', 'r', encoding='UTF-8').read()

example_letter = get_letters_frequency(example_text)
encoded_letter = get_letters_frequency(encoded_text)

words = get_words(example_text)
encoded_words = get_words(encoded_text)

sorted_sample_chars = sorted(example_letter.items(), key=lambda x: -x[1])
sorted_encoded_letters = sorted(encoded_letter.items(), key=lambda x: -x[1])

example_letter = dict(sorted_sample_chars)
encoded_letter = dict(sorted_encoded_letters)
print("\nfrequency of letters from kyrgyz text txt: ")
print(example_letter)
print("\nfrequency of letters from input text: ")
print(encoded_letter)

key = dict()

for k in encoded_letter:
    key[k] = None

key[sorted_encoded_letters[0][0]] = sorted_sample_chars[0][0]


uq_text = ' '.join(words)


checked_words = set()

while None in key.values():

    best_matches = []

    for encoded_word in encoded_words:

        if encoded_word in checked_words:
            continue

        pattern = r''
        for s in encoded_word:
            if key.get(s) is not None:
                pattern += key.get(s)
            else:
                pattern += f"[{''.join((c for c in alph if c not in key.values() and abs((example_letter.get(c, 100000) / encoded_letter.get(s, 1)) - 1) < 2))}]"
        pattern += '$'

        candidates = list(filter(lambda w: re.match(pattern, w), words))

        candidates = list(filter(lambda w: check(w, encoded_word), candidates))

        updated_chars = set()

        if len(candidates) == 1:
            real_word_candidate = candidates[0]

            error = 0

            for i in range(len(encoded_word)):
                error += 0 if key[encoded_word[i]] is None \
                    else encoded_letter.get(encoded_word[i], 0) * 1.0 / example_letter.get(real_word_candidate[i], 1)
            if error != 0:
                best_matches.append((encoded_word, real_word_candidate, error / len(encoded_word)))



    best_matches.sort(key=lambda x: x[2])

    if len(best_matches) == 0:
        break
    print("    candidate:    encoded:   score: ")
    for encoded_word, real_word_candidate, err in best_matches[:10]:
        word_list = list(encoded_word)
        candidate_list = list(real_word_candidate)

        for b, a in zip(candidate_list, word_list):
            key[a] = b

        checked_words.add(encoded_word)

        print( "   ", real_word_candidate, "   ", encoded_word, "   ", round(err, 4))

    print("\nnext iteration...\n")

text = ''

for letter in encoded_text:
    if letter.isalpha():
        is_upper = letter != letter.lower()
        letter = letter.upper()
        text += (key[letter].lower() if not is_upper else key[letter].upper()) if key.get(letter, None) is not None else '_'
    else:
        text += letter

print(text)