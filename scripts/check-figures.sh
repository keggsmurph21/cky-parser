#!/usr/bin/env bash
#
# Kevin Murphy
# Spring 2019
# Linguistics Honors project
#

set -e

echo "checking examples"
#python src/main.py get -i cess_cat -n 10
#python src/main.py draw -i cess_esp -n 6
python src/main.py induce -i cess_cat -n 100
python src/main.py induce -i cess_esp -n 200 -o /tmp/induced
python src/main.py normalize -i cess_cat -n 10
python src/main.py normalize -g /tmp/induced -n 10
python src/main.py normalize -g /tmp/induced -n 10 -o /tmp/normalized
python src/main.py add-lexicon -i cess_esp -n 10 -l cess_esp\
    -c /tmp/tags.json
python src/main.py add-lexicon -i cess_esp -n 10 -l cess_cat\
    -c /tmp/tags.json
python src/main.py add-lexicon -g /tmp/induced -n 10 -c /tmp/tags.json
python src/main.py add-lexicon -g /tmp/normalized -n 10 -c /tmp/tags.json
python src/main.py parse -i cess_cat -n 2 -l cess_esp
python src/main.py parse -c /tmp/tags.json -n 2 -l cess_esp
python src/main.py add-lexicon -i cess_esp -n 1 -l cess_cat\
    -c /tmp/esp1cat.json
python src/main.py add-lexicon -i cess_esp -n 2 -l cess_cat\
    -c /tmp/esp2cat.json
python src/main.py add-lexicon -i cess_esp -n 3 -l cess_cat\
    -c /tmp/esp3cat.json
python src/main.py add-lexicon -i cess_cat -n 3 -l cess_cat\
    -c /tmp/cat3cat.json
python -i src/main.py add-lexicon -l cess_cat -n 3\
    --test /tmp/esp*cat.json --truth /tmp/cat3cat.json

echo "inducing on 1,5,10,50"
python src/main.py induce -c cess_cat -n 1 | wc -l
python src/main.py induce -c cess_cat -n 5 | wc -l
python src/main.py induce -c cess_cat -n 10 | wc -l
python src/main.py induce -c cess_cat -n 50 | wc -l

echo "normalizing on 1,5,10,50"
python src/main.py normalize -c cess_cat -n 1 | wc -l
python src/main.py normalize -c cess_cat -n 5 | wc -l
python src/main.py normalize -c cess_cat -n 10 | wc -l
python src/main.py normalize -c cess_cat -n 50 | wc -l

echo "run cess_cat tests"
python src/main.py analyze --test cache/cess_esp*-cess_cat-tags.json --truth cache/cess_cat100-cess_cat-tags.json -l cess_cat -n100

echo "run cess_esp tests"
python src/main.py analyze --test cache/cess_cat*-cess_esp-tags.json --truth cache/cess_esp100-cess_esp-tags.json -l cess_esp -n100
