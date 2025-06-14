import json
import nltk
from nltk.corpus import gutenberg, words as nltk_words, wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download("gutenberg")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("words")

lemmatizer = WordNetLemmatizer()
english_words = set(w.lower() for w in nltk_words.words())

words = [w.lower() for w in gutenberg.words() if w.isalpha() and len(w) > 2]
word_freq = Counter(words)
tagged = pos_tag(words)

nouns, verbs, adjs, advs = set(), set(), set(), set()

# === MANUAL BLACKLIST ===
boring_words = {
    "thing", "stuff", "nice", "fun", "big", "small", "bad", "good", "get", "got",
    "make", "made", "go", "went", "say", "said", "see", "seen", "guy", "girl", "boy",
    "come", "came", "people", "really", "very", "okay"
}

# === POS MAPPER ===
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

# === PROCESS LOOP ===
for word, tag in tagged:
    if word in boring_words:
        continue
    if tag in ["NNP", "NNPS"]:  # Skip proper nouns
        continue

    pos = get_wordnet_pos(tag)
    if not pos:
        continue

    lemma = lemmatizer.lemmatize(word, pos)

    if lemma not in english_words:
        continue

    # exclude overly common or overly rare words
    freq = word_freq[lemma]
    if freq < 2 or freq > 400:
        continue

    # Assign to POS buckets
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
