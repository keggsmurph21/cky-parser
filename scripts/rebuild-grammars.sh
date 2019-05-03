#!/usr/bin/env bash
#
# Kevin Murphy
# Spring 2019
# Linguistics Honors project
#

set -e # exit script if a command fails

CORPORA='cess_esp cess_cat'
GRAMMAR_DIR='./grammars'

for parse_corpus in $CORPORA; do
    
    for num_sents in 1 10 100 1000; do

        raw_grammar="$GRAMMAR_DIR/$parse_corpus$num_sents.txt"
        cnf_grammar="$GRAMMAR_DIR/$parse_corpus$num_sents-cnf.txt"

        echo "inducing \"$raw_grammar\"" >&2
        python src/main.py induce \
            --corpus $parse_corpus \
            -n $num_sents \
            >$raw_grammar \
            2>/dev/null

        echo "normalizing \"$cnf_grammar\"" >&2
        python src/main.py normalize \
            --grammar $raw_grammar \
            -n $num_sents \
            >$cnf_grammar

        for lex_corpus in $CORPORA; do

            tag_file="$GRAMMAR_DIR/$parse_corpus$num_sents-$lex_corpus-tags.json"

            echo "adding lexicon \"$tag_file\"" >&2
            python src/main.py add-lexicon \
                --grammar $cnf_grammar \
                --lexicon $lex_corpus \
                -n $num_sents \
                --json $tag_file

        done

    done
    
    raw_grammar="$GRAMMAR_DIR/$parse_corpus.txt"
    cnf_grammar="$GRAMMAR_DIR/$parse_corpus-cnf.txt"

    echo "inducing \"$raw_grammar\"" >&2
    python src/main.py induce \
        --corpus $parse_corpus \
        >$raw_grammar \
        2>/dev/null

    echo "normalizing \"$cnf_grammar\"" >&2
    python src/main.py normalize \
        --grammar $raw_grammar \
        >$cnf_grammar

    for lex_corpus in $CORPORA; do

        tag_file="$GRAMMAR_DIR/$parse_corpus-$lex_corpus-tags.json"

        echo "adding lexicon \"$tag_file\"" >&2
        python src/main.py add-lexicon \
            --grammar $cnf_grammar \
            --lexicon $lex_corpus \
            --json $tag_file

    done

done

echo "grammars:"
wc -l "$GRAMMAR_DIR/*" | grep -v 'total' | sort -rh

