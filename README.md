# poem-p1

![CLI-output of a poem](/assets/poem_screenshot.webp "A janky poem")

A small command-line tool that generates strange little poems from your keywords. It fills in simple templates using words from a filtered NLTK Gutenberg corpus, with word choice biased toward vowel overlap (assonance). The results are often broken, surreal, but sometimes interesting.

### Usage

```bash
python poem_generator.py [keywords] [--options]
```

Options:
- `--repeat N` repeats the keyword cycle `N` times (default: 1).
- `--seed N` Set random seed. The seed is about the line template used, so it has nothing to do with words choices.
- `--out FILE` Write to file instead of stdout.

Example usage:


### Setup

Requires Python3 and `nltk`.

You need to generate the wordbank at first:

```bash
python generate_wordbank.py
```

Then run `main.py` with whatever keywords you want, e.g.,
```bash
python poem_generator.py sorrow field bell --repeat 2 --seed 42
```


