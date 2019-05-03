#!/usr/bin/env bash

set -e

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
