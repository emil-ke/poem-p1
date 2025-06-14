import json
import random
import re

# === CONFIG ===
VOWEL_BIAS_CHANCE = 0.8


with open("wordbank.json") as f:
    wordbank = json.load(f)

nouns = wordbank["nouns"]
verbs = wordbank["verbs"]
adjs = wordbank["adjs"]
advs = wordbank["advs"]


templates = [
    "the {noun} {verb}s the {noun}",
    "a {noun} {verb}s beneath the {noun}",
    "{noun}s {verb} in {noun}",
    "the {noun} and the {noun} {verb}",
    "before the {noun}, a {noun} {verb}s",
    "{noun} without {noun}",
    "{noun} {verb}s {noun}",
    "O slow, O so {adj}",
    "between {noun} and {noun}, {noun} {verb}s",
    "{noun}s {verb} toward the {noun}",
    "people or {noun}, {adv}",
    "under {noun}, the {noun} {verb}s",
    "in the {noun}, {noun}s {verb}",
    "{adj} {noun}, and the {noun} {verb}s",
    "{noun} {verb}s alone",
    "where {noun} {verb}s, the {noun} waits",
    "the {noun} was {verb}ed by the {noun}",
    "{noun}, and then nothing",
    # (polysyndeton)
    "{noun} and {noun} and {noun} {verb}",
    "{noun} or {noun} or {noun}, {verb}ing still",
    "O {noun} and O {noun}, and still the {noun} {verb}s",
    "{adj}, and {adj}, and {adj} {noun}s",
]


def get_first_vowel(word):
    for c in word:
        if c in "aeiou":
            return c
    return None


def biased_vowel_choice(bank, keyword_vowel=None, vowel_chance=VOWEL_BIAS_CHANCE):
    if keyword_vowel and random.random() < vowel_chance:
        filtered = [w for w in bank if get_first_vowel(w) == keyword_vowel]
        if filtered:
            return random.choice(filtered)
    return random.choice(bank)


def clean_suffix_overflow(line):
    # This is a bit janky, which is fine for now

    # Fix triple or more 's' at word ends (e.g., "kisss" → "kiss")
    line = re.sub(r'\b(\w*?)s{3,}\b', r'\1ss', line)

    # Fix past tense double "eded" (like "walkeded")
    line = re.sub(r'(\w+)eded\b', r'\1ed', line)
    
    # (e.g. "douseed" -> "doused")
    line = re.sub(r'(\w+)eed\b', r'\1ed', line)

    # (e.g. "supplys" -> "supplies")
    line = re.sub(r'(\w+)lys\b', r'\1lies', line)

    # (e.g., "crucifys" -> "crucifies")
    line = re.sub(r'(\w+)fys\b', r'\1fies', line)

    return line

def fix_articles(line):
    # Replace "a [vowel]" with "an [vowel]"
    return re.sub(r'\ba ([aeiouAEIOU])', r'an \1', line)


def generate_line_with_keyword(keyword):
    # Determine POS for the keyword
    pos = "noun"
    if keyword.endswith("ly"):
        pos = "adv"
    elif keyword in adjs:
        pos = "adj"
    elif keyword in verbs or keyword.endswith("ing"):
        pos = "verb"
    else:
        pos = "noun"

    # Filter templates that contain at least one matching placeholder
    matching_templates = [t for t in templates if f"{{{pos}}}" in t]
    if not matching_templates:
        return f"[no template for {keyword}]"

    template = random.choice(matching_templates)

    placeholders = {
        "noun": len(re.findall(r"{noun}", template)),
        "verb": len(re.findall(r"{verb}", template)),
        "adj":  len(re.findall(r"{adj}", template)),
        "adv":  len(re.findall(r"{adv}", template)),
    }

    keyword_letter = keyword[0]
    keyword_vowel = get_first_vowel(keyword)

    fill = {}
    for tag in placeholders:
        bank = wordbank[tag + "s"]
        fill[tag] = [
            biased_vowel_choice(bank, keyword_vowel, VOWEL_BIAS_CHANCE)
            for _ in range(placeholders[tag])
        ]

    # Guaranteed insertion
    i = random.randint(0, placeholders[pos] - 1)
    fill[pos][i] = keyword

    for tag in fill:
        for rep in fill[tag]:
            template = template.replace("{" + tag + "}", rep, 1)

    res = clean_suffix_overflow(template)
    res = fix_articles(template)
    return res

def main():
    keywords_input = input("Enter keywords (comma-separated): ")
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
    random.shuffle(keywords)

    print("\n")
    for i, kw in enumerate(keywords):
        print(generate_line_with_keyword(kw))
        if (i + 1) % 4 == 0:
            print()


if __name__ == "__main__":
    main()
