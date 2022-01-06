#!/bin/bash

# This script performs significance testing for the different model
# combinations.

# First argument must be "german" or "dutch"
language=$1
search_term=$2

BIN_DIR="statistics/binary_results/$language/$search_term"
SIGN_TEST_FILE="statistics/significance_test_results_"$language"_"$search_term".tsv"

echo -n > $SIGN_TEST_FILE

for file1 in $(ls $BIN_DIR)
do
    for file2 in $(ls $BIN_DIR)
    do
        if [ $file1 != $file2 ]
        then
            python3 scripts/testSignificance.py "$BIN_DIR/$file1" "$BIN_DIR/$file2" 0.05 "$SIGN_TEST_FILE"
        fi
    done
done
