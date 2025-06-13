import json
import nltk
from nltk.corpus import brown, words as nltk_words, wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

nltk.download("brown")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger_eng")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("words")

english_words = set(w.lower() for w in nltk_words.words())
lemmatizer = WordNetLemmatizer()
words = brown.words()
tagged = pos_tag(words)

nouns, verbs, adjs, advs = set(), set(), set(), set()

def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    return None

for word, tag in tagged:
    word = word.lower()
    if len(word) < 3 or not word.isalpha():
        continue
    if tag in ["NNP", "NNPS"]:  # Skip proper nouns
        continue

    pos = get_wordnet_pos(tag)
    if not pos:
        continue

    lemma = lemmatizer.lemmatize(word, pos)
    if lemma not in english_words:
        continue

    if pos == wordnet.NOUN:
        nouns.add(lemma)
    elif pos == wordnet.VERB:
        verbs.add(lemma)
    elif pos == wordnet.ADJ:
        adjs.add(lemma)
    elif pos == wordnet.ADV:
        advs.add(lemma)

wordbank = {
    "nouns": sorted(nouns),
    "verbs": sorted(verbs),
    "adjs": sorted(adjs),
    "advs": sorted(advs)
}

with open("wordbank.json", "w") as f:
    json.dump(wordbank, f, indent=2)

print("Wordbank saved to wordbank.json")
