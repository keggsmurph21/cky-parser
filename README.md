# cky-parser

This program contains a bundle of computational linguistic tools developed
by Kevin Murphy for a Swarthmore College Honors project in Spring 2019.  This
repository provides implementations for several tools related to NLTK
(https://www.nltk.org/).

## usage

 - to print a bracket-notation parse of a sentence from the nltk.cess_cat or
   nltk.cess_esp corpora to the console, type:

    ```bash
    $ python src/main.py get -i cess_cat -n 10
    ```

- to draw a parsed sentence from either of these corpora, type:

    ```bash
    $ python src/main.py draw -i cess_esp -n 6
    ```

- to induce a grammar from a (subset of) cess_cat/cess_esp, try

    ```bash
    $ python src/main.py induce -i cess_cat -n 100 # writes to stdout
    $ python src/main.py induce -i cess_esp -n 200 -o /tmp/induced.txt
    ```

- to normalize an induced grammar (into Chomsky Normal Form):

    ```bash
    $ python src/main.py normalize -i cess_cat -n 10   # induce then normalize
    $ python src/main.py normalize -g /tmp/induced -n 10    # read in
    $ python src/main.py normalize -g /tmp/induced -n 10 -o /tmp/normalized.txt
    ```

- prepare a grammar for parsing:

    ```bash
    $ python src/main.py add-lexicon -i cess_esp -n 10 -l cess_esp\
        -c /tmp/tags.json
    $ python src/main.py add-lexicon -i cess_esp -n 10 -l cess_cat\
        -c /tmp/tags.json
    $ python src/main.py add-lexicon -g /tmp/induced -n 10 -c /tmp/tags.json
    $ python src/main.py add-lexicon -g /tmp/normalized -n 10 -c /tmp/tags.json
    ```

- run the CKY parser with a grammar and a lexicon

    ```bash
    $ python src/main.py parse -i cess_cat -n 2 -l cess_esp
    $ python src/main.py parse -c /tmp/tags.json -n 2 -l cess_esp
    ```

- run some statistical analysis on the resultant performance of the parser
  NB: currently this outputs in pseudo-`LaTeX`, which is not particularly
  enlightening; if you'd like to dig in deeper, try running the program
  interactively (i.e. see line 5 below) & you'll have the results available
  on the console as "test_results"

    ```bash
    $ python src/main.py add-lexicon -i cess_esp -n 1 -l cess_cat\
        -c /tmp/esp1cat.json
    $ python src/main.py add-lexicon -i cess_esp -n 2 -l cess_cat\
        -c /tmp/esp2cat.json
    $ python src/main.py add-lexicon -i cess_esp -n 3 -l cess_cat\
        -c /tmp/esp3cat.json
    $ python src/main.py add-lexicon -i cess_cat -n 3 -l cess_cat\
        -c /tmp/cat3cat.json
    $ python -i src/main.py add-lexicon -l cess_cat -n 3\
        --test /tmp/esp*cat.json --truth /tmp/cat3cat.json
        ```

## installation

```bash
git clone https://github.com/keggsmurph21/cky-parser
cd cky-parser
pip install --user -r requirements.txt
python src/main.py --help
```


Kevin Murphy, 2019 (GPLv3+)
