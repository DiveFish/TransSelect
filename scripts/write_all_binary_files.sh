#!/bin/bash

filtered_file=$1
language=$2
search_term=$3

PRED_DIR=$"predictions/$language/$search_term/"
BIN_DIR=$"statistics/binary_results/$language/$search_term/"

if [ ! -d "$BIN_DIR" ]
then
    mkdir "$BIN_DIR"
fi

for pred_file in $(ls $PRED_DIR)
do
    bin_file=$(echo $pred_file | cut -d "." -f 1)
    out_path="$BIN_DIR/binary-$bin_file"
    python3 scripts/binary_output_per_sentence.py "$PRED_DIR$pred_file" $filtered_file $out_path
done
