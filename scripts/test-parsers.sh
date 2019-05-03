#!/usr/bin/env bash
#
# Kevin Murphy
# Spring 2019
# Linguistics Honors project
#

set -e # exit script if a command fails

train_corpus="$1"
test_corpus="$2"
n="$3"

if [ -z $1 ]; then
    echo "no training corpus specified"
fi

if [ -z $2 ]; then
    echo "no testing corpus specified"
fi

if [ -z $3 ]; then

    python src/main.py parse -j "grammars/$train_corpus-$test_corpus-tags.json" -l "$test_corpus"

else

    python src/main.py parse -j "grammars/$train_corpus-$test_corpus-tags.json" -l "$test_corpus" -n "$n"

fi
